import logging

from fastapi import WebSocket

logger = logging.getLogger(__name__)


class ConnectionManager:
    def __init__(self):
        self.connections: set[WebSocket] = set()

    async def connect(self, websocket: WebSocket) -> None:
        await websocket.accept()
        self.connections.add(websocket)

        logger.info(
            "websocket_connected connections=%s",
            len(self.connections),
        )

    def disconnect(self, websocket: WebSocket) -> None:
        self.connections.discard(websocket)

    @staticmethod
    async def send(websocket: WebSocket, message: dict):
        await websocket.send_json(message)
