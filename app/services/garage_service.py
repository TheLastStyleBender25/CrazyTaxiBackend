from sqlalchemy.orm import Session
from starlette import status
from app.models import Player, OwnedTaxi, AvailableTaxi
from fastapi import Depends, HTTPException
from app.services.transaction_service import create_transaction
from app.core.logger import logger

def buy_taxi(db: Session, current_user, taxi_id):
    player = db.query(Player).filter(Player.user_id == current_user.id).first()
    taxi = db.query(AvailableTaxi).filter(AvailableTaxi.id == taxi_id).first()
    if not taxi:
        logger.error(f"No taxi found for {taxi_id}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No available taxi")
    if player.coins < taxi.price:
        logger.error(f"player coins are less than taxi price for {taxi_id}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not enough coins")
    player.coins -= taxi.price

    owned_taxi_player = OwnedTaxi(player_id = player.id, taxi_id = taxi.id, taxi_type = taxi.taxi_type, fuel = taxi.fuel, health = taxi.health, is_active = False, fuel_cost_per_km = taxi.fuel_cost_per_km, health_cost_per_km = taxi.health_cost_per_km)
    create_transaction(db, player.id, -taxi.price, "purchase", f"purchased {taxi.taxi_type}")

    db.add(owned_taxi_player)
    db.commit()

    return {"Taxi purchased successfully":taxi.id}

def get_available_all_taxis(db):
    owned_taxi_players = db.query(AvailableTaxi).all()
    return owned_taxi_players

def get_owned_all_taxis(db, current_user):
    player = db.query(Player).filter(Player.user_id == current_user.id).first()
    taxis = db.query(OwnedTaxi).filter(player.id == OwnedTaxi.player_id).all()
    return taxis

def get_available_taxis_for_buy(db, current_user):
    player = db.query(Player).filter(Player.user_id == current_user.id).first()
    owned = db.query(OwnedTaxi).filter(player.id == OwnedTaxi.player_id).all()
    owned_list=[]
    for owned_taxi in owned:
        owned_list.append(owned_taxi.taxi_id)
    available = db.query(AvailableTaxi).filter(~AvailableTaxi.id.in_(owned_list)).all()
    return available

