from fastapi import WebSocket
from app.core.logger import logger

class ConnectionManager:
    def __init__(self):
        # Dictionary that stores:
        #
        # {
        #    player_id : websocket_connection
        # }
        #
        self.active_connections = {}

    async def connect(self, player_id,websocket: WebSocket):
        # Accepts websocket connection.
        #
        # Without this line,
        # websocket connection will stay pending.
        await websocket.accept()

        # Save websocket connection
        # using player_id as key.
        #
        # Example:
        # self.active_connections["player123"] = websocket
        logger.info(f"Accepted connection from {player_id}")
        self.active_connections[player_id] = websocket

    def disconnect(self,player_id):
        # Remove disconnected player's websocket.
        #
        # Prevents memory leaks
        # and dead socket references.
        if player_id in self.active_connections:
            del self.active_connections[player_id]


    # Sends realtime message to one player.
    #
    # Example:
    # - new ride added
    # - ride expired
    # - reward update
    async def send_personal_message(self, player_id, message):
        websocket = self.active_connections.get(player_id)
        if websocket:
            try:
                await websocket.send_json(message)
            except Exception:
                logger.info("disconnecting websocket")
                self.disconnect(player_id)



# Global shared manager object.
#
# Entire backend will use this single instance
# to manage all websocket connections.
manager = ConnectionManager()





