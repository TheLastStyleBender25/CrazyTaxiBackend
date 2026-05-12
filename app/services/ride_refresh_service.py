import asyncio
import app.websocket.connection_manager as manager
from app.core.logger import logger
from app.services.ride_service import refresh_ride_pool
from app.db.session import SessionLocal
from app.models import User
from app.core.config import RIDE_REFRESH_INTERVAL

async def ride_refresh_loop():
    logger.info("ride loop started")
    while True:
        try:
            await asyncio.sleep(RIDE_REFRESH_INTERVAL)
            active_players = list(manager.manager.active_connections.keys())
            db = SessionLocal()
            try:
                for player in active_players:
                    try:
                        current = db.query(User).filter(User.id == player).first()
                        if not current:
                            continue
                        refresh = refresh_ride_pool(db, current)
                        await manager.manager.send_personal_message(player, {"event": "ride_refresh", "rides" : refresh})
                    except Exception as e:
                        logger.error(f"Ride refresh failed for "f"player {player}: {str(e)}")
            finally:
                db.close()
        except Exception as e:
            logger.error(f"Ride refresh loop crashed: {str(e)}")
