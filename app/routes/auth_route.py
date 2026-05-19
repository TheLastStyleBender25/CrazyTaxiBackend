from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import  Session
from app.db.session import get_db
from app.core.security import create_token, create_refresh_token
from app.services.auth_service import register_user, authenticate_user, rotate_refresh_token, get_data_of_player
from app.schemas.auth import LoginUser, RegisterUser, RefreshTokenRequest
from app.core.security import get_current_user
from app.core.limiter import limiter
from fastapi import Request
from app.core.logger import logger
from app.services.email_service import verify_email_user

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register")
@limiter.limit("3 per minute")
def register(request : Request, data : RegisterUser, db: Session = Depends(get_db)):
    try:
        user = register_user(db, data.email, data.password)
    except ValueError as e:
        logger.error(e)
        raise HTTPException(status_code=400, detail=str(e))

    return {"email": user.email, "created" : "successfully. Please verify!"}


@router.post("/login")
@limiter.limit("5 per minute")
def login(request : Request, data : LoginUser, db: Session = Depends(get_db)):
    try:
        response = authenticate_user(db, data.email, data.password)
        return response
    except ValueError as e:
        logger.error(e)
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/refresh")
def refresh(data : RefreshTokenRequest, db: Session = Depends(get_db)):
    try:
        tokens = rotate_refresh_token(db, data.refresh_token)
        return tokens
    except ValueError as e:
        logger.error(e)
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/me")
def me(current_user = Depends(get_current_user)):
    return current_user

@router.get("/verify-email")
def verify_email(token: str,db: Session = Depends(get_db)):
    try:
        email = verify_email_user(token, db)
        return { "email" : "verified. Please log in"}
    except ValueError as e:
        logger.error(e)
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/player_data")
def get_player_data(token:str, db: Session = Depends(get_db)):
    try:
        player_data = get_data_of_player(db, token)
        return player_data
    except ValueError as e:
        logger.error(e)
        raise HTTPException(status_code=400, detail=str(e))
