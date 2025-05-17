from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, WebSocket] = {}

    async def connect(self, username: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[username] = websocket

    def disconnect(self, username: str):
        self.active_connections.pop(username, None)

    async def broadcast(self, sender: str, message: str):
        for user, ws in self.active_connections.items():
            if user != sender:
                await ws.send_text(f"{sender}: {message}")

manager = ConnectionManager()