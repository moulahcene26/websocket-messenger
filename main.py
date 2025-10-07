from fastapi import FastAPI, WebSocket, WebSocketDisconnect


app = FastAPI()


class ConnectionManager:
    def __init__(self):
        self.active_connections = []


    async def connect(self, websocket: WebSocket, username: str):
        await websocket.accept()
        self.active_connections.append({"websocket": websocket, "username":username})
        await manager.broadcast(f"+ {username} joined the chat")

    def disconnect(self, websocket: WebSocket):
        user = next((conn for conn in self.active_connections if conn["websocket"] == websocket), None)
        if user:
            self.active_connections.remove(user)
            return user["username"]
        return None

    async def broadcast(self, message:str):
        for connection in self.active_connections:
            await connection["websocket"].send_text(message)




manager = ConnectionManager()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    username=websocket.query_params.get("username") or "Anonymous"
    await manager.connect(websocket, username)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"{username}: {data}")
    except WebSocketDisconnect:
        user_left = manager.disconnect(websocket)
        if user_left:
            await manager.broadcast(f"- {user_left} left the chat")

