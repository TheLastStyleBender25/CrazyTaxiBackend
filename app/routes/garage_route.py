from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.security import get_current_user
from app.models import User
from app.services.garage_service import buy_taxi, get_available_all_taxis, get_owned_all_taxis, get_available_taxis_for_buy

router = APIRouter(prefix="/garage", tags=["garage"])

@router.post("buy/{taxi_id}")
def buy_taxi_by_player(taxi_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return buy_taxi(db, current_user, taxi_id)

@router.get("/available")
def get_available_taxis(db:Session = Depends(get_db), current_user = Depends(get_current_user)):
    return get_available_all_taxis(db)

@router.get("/owned_taxis")
def get_owned_taxis(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return get_owned_all_taxis(db, current_user)

@router.get("taxis_available_for_buy")
def get_available_taxis_to_buy(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return get_available_taxis_for_buy(db, current_user)