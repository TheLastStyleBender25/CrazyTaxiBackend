from fastapi import APIRouter, HTTPException
from fastapi import Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.milestone_service import claim_milestone, get_claimable_milestones
from app.core.security import get_current_user
from app.models import Player
from fastapi import Request
from app.core.limiter import limiter
from app.core.logger import logger

router = APIRouter(prefix="/milestones",tags=["Milestones"])

@router.get("/claimable")
def get_claimable(current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    player = db.query(Player).filter(Player.user_id == current_user.id).first()
    try:
        result = get_claimable_milestones(db, player)
        return result
    except ValueError as e:
        logger.error(e)
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/claim/{milestone_id}")
@limiter.limit("3 per minute")
def claim(request : Request, milestone_id: int, current_user = Depends(get_current_user),db: Session = Depends(get_db)):
    player = db.query(Player).filter(Player.user_id == current_user.id).first()
    try:
        result = claim_milestone(db, player, milestone_id)
        return result
    except ValueError as e:
        logger.error(e)
        raise HTTPException(status_code=400, detail=str(e))
