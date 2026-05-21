from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import  Session
from app.core.logger import logger
from app.db.session import get_db
from app.models import Player
from app.core.security import get_current_user
from app.services.city_service import unlock_next_city, get_city_level_all
from app.core.limiter import limiter
from fastapi import Request

router = APIRouter(prefix="/cities",tags=["Cities"])

@router.post("/unlock")
@limiter.limit("2 per minute")
def unlock_city(request : Request, current_user = Depends(get_current_user),db: Session = Depends(get_db)):
    player = db.query(Player).filter(Player.user_id == current_user.id).first()
    try:
        result = unlock_next_city(db, player)
        return result
    except ValueError as e:
        logger.error(e)
        raise HTTPException(status_code=400, detail=str(e))




@router.get("/city_level")
@limiter.limit("6 per minute")
def get_city_level(request : Request, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        cities = get_city_level_all(db)
        return cities
    except ValueError as e:
        logger.error(e)
        raise HTTPException(status_code=400, detail=str(e))
