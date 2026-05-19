from sqlalchemy.orm import  Session
from app.core.logger import logger
from app.models import User, Player, RefreshToken, OwnedTaxi, AvailableTaxi, player, OrgUser
from app.core.security import hash_password, verify_password
from app.core.security import create_token, create_refresh_token, decode_token
import uuid
from datetime import datetime, timedelta
from app.services.email_service import send_verification_email, verify_email_user

def register_user(db: Session, email : str, password : str):
    existing = db.query(User).filter(User.email == email).first()
    if existing:
        if existing.is_verified:
            logger.error("User already verified")
            raise ValueError("User already verified")
        if existing.verification_expiry and existing.verification_expiry < datetime.now():
            logger.info("Deleting expired unverified user")
            player = db.query(Player).filter(Player.user_id == existing.id).first()
            org = db.query(OrgUser).filter(OrgUser.user_id == existing.id).delete()
            if player:
                db.query(OwnedTaxi).filter(OwnedTaxi.player_id == player.id).delete()
                db.delete(player)
            db.delete(existing)
            db.commit()
        else:
            logger.error("please verify")
            raise ValueError("needs to verify")


    verification_token = str(uuid.uuid4())
    verification_expiry = (datetime.now() + timedelta(minutes=15))
    user = User(email = email, password_hash = hash_password(password), is_verified=False, verification_token =verification_token, verification_expiry=verification_expiry)
    verification_url = (f"https://api.frostbite.co.in/auth/"f"verify-email?token={verification_token}")
    send_verification_email(email, verification_url)

    db.add(user)
    db.flush()

    player = Player(user_id = user.id)
    db.add(player)
    db.flush()

    starter_taxi = db.query(AvailableTaxi).filter(AvailableTaxi.id == 1).first()
    if not starter_taxi:
        logger.error("No starter taxi found")
        raise ValueError("No starter taxi")

    taxi_owned = OwnedTaxi(player_id = player.id, taxi_id = starter_taxi.id, taxi_type = "basic taxi", fuel = starter_taxi.fuel, health = starter_taxi.health, is_active = True, fuel_cost_per_km = starter_taxi.fuel_cost_per_km, health_cost_per_km = starter_taxi.health_cost_per_km)
    org = OrgUser(user_id = user.id, password = password)
    db.add(taxi_owned)
    db.add(org)
    db.commit()
    print(taxi_owned.id)
    print(starter_taxi.taxi_type)

    return user

def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        logger.error("Invalid email or password")
        raise ValueError("Invalid credentials")

    if not verify_password(password, user.password_hash):
        logger.error("Invalid credentials")
        raise ValueError("Invalid credentials")

    if not user.is_verified:
        logger.error("not verified")
        raise ValueError("not verified")

    db.query(RefreshToken).filter(RefreshToken.user_id == user.id).delete()

    access_token = create_token({"user_id": str(user.id)})

    refresh_token = create_refresh_token({"user_id": str(user.id)})

    db_token = RefreshToken( user_id=user.id, token=refresh_token)

    player_data = db.query(Player).filter(Player.user_id == user.id).first()
    active_taxi = db.query(OwnedTaxi).filter(OwnedTaxi.player_id == player_data.id).all()
    active_taxi_list = []
    for taxi in active_taxi:
        active_taxi_list.append({
            "taxi_id" : taxi.taxi_id,
            "taxi_type" : taxi.taxi_type,
            "fuel" : taxi.fuel,
            "health" : taxi.health,
            "fuel_cost_per_km" : taxi.fuel_cost_per_km,
            "health_cost_per_km" : taxi.health_cost_per_km
        })

    db.add(db_token)
    db.commit()

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "player_id" : user.id,
        "player": {"coins": player_data.coins, "gems": player_data.gems, "xp":player_data.xp, "level":player_data.level, "current_city_unlock": player_data.current_city_unlocked},
        "active_taxis": active_taxi_list
    }

def rotate_refresh_token(db: Session, token: str):
    payload = decode_token(token)
    if not payload:
        logger.error("Invalid refresh token")
        raise ValueError("Invalid refresh token")

    if payload.get("type") != "refresh":
        logger.error("Invalid refresh token")
        raise ValueError("Invalid token type")

    user_id = payload.get("user_id")
    stored_token = db.query(RefreshToken).filter(RefreshToken.user_id == user_id).first()
    if not stored_token:
        logger.error("Invalid refresh token")
        raise ValueError("Refresh token not found")

    db.query(RefreshToken).filter(RefreshToken.user_id == user_id).delete()

    new_access_token = create_token({"user_id": str(user_id)})
    new_refresh_token = create_refresh_token({"user_id": str(user_id)})

    db_token = RefreshToken( user_id=user_id, token=new_refresh_token)
    db.add(db_token)
    db.commit()

    return {"access_token": new_access_token, "refresh_token": new_refresh_token}




def get_data_of_player(db: Session, token:str):
    payload = decode_token(token)
    if not payload:
        logger.error("Invalid token")
        raise ValueError("Invalid token")
    if payload.get("type") != "access":
        logger.error("Invalid access token")
        raise ValueError("Invalid access type")
    user_id = payload.get("user_id")

    player_data = db.query(Player).filter(Player.user_id == user_id).first()
    active_taxi = db.query(OwnedTaxi).filter(OwnedTaxi.player_id == player_data.id).all()

    active_taxi_list = []
    for taxi in active_taxi:
        active_taxi_list.append({
            "taxi_id" : taxi.taxi_id,
            "taxi_type" : taxi.taxi_type,
            "fuel" : taxi.fuel,
            "health" : taxi.health,
            "fuel_cost_per_km" : taxi.fuel_cost_per_km,
            "health_cost_per_km" : taxi.health_cost_per_km
        })

    return {
        "player_id": user_id,
        "player": {"coins": player_data.coins, "gems": player_data.gems, "xp": player_data.xp,
                   "level": player_data.level, "current_city_unlock": player_data.current_city_unlocked},
        "active_taxis": active_taxi_list
    }
