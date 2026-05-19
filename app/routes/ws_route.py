from fastapi import WebSocket
from fastapi import APIRouter
from fastapi import WebSocketDisconnect
from redis.commands.search import result
from app.websocket.connection_manager import manager
from app.db.session import SessionLocal
from app.models import User
from app.services.ride_service import generate_ride_pool, get_ride_pool, accept_ride, complete_rides
import asyncio



router = APIRouter(prefix="/ws", tags=["Websocket"])

@router.websocket("/rides_pool/{player_id}")
async def websocket_endpoint(websocket: WebSocket, player_id: str):
    db = SessionLocal()
    current = db.query(User).filter(User.id == player_id).first()
    await manager.connect(player_id, websocket)
    await asyncio.sleep(3)

    rides = get_ride_pool(current)
    if not rides:
        rides = generate_ride_pool(db, current)
    await  manager.send_personal_message(player_id,{"event" : "rides_pool", "rides" : rides})
    try:
        while True:
            # Wait for client message
            #
            # Currently we don't process
            # incoming websocket messages.
            #
            # This simply keeps connection alive.
            data = await websocket.receive_json()

            # ====================================
            # ACCEPT RIDE EVENT
            # ====================================
            event = data.get("event")
            if event == "accept_ride":
                try:
                    ride_id = data.get("ride_id")
                    taxi_id = data.get("taxi_id")
                    result = accept_ride(db, current, taxi_id, ride_id)
                    await manager.send_personal_message(player_id, {"event": "ride_accepted", "ride": result["accepted_ride"]})
                except Exception as e:
                    await manager.send_personal_message(player_id, {"event" : "error", "error": str(e)})

            # ====================================
            # COMPLETE RIDES EVENT
            # ====================================
            if event == "complete_rides":
                try:
                    _rides = data.get("rides")
                    result = complete_rides(db, current, _rides)
                    await manager.send_personal_message(player_id, {"event": "rides_completed", "completed_rides": result["completed_rides"], "reward": result["reward_earned"], "coins": result["coins"]})
                except Exception as e:
                    await manager.send_personal_message(player_id, {"event" : "error", "error": str(e)})

    except WebSocketDisconnect:
        manager.disconnect(player_id)

