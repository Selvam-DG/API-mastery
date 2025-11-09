from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .config import settings
from .logger import log
from .schemas import WSInMessage, WSOutMessage
from .utils import require_query_params
from .ws_manager import WSConnection, manager


app = FastAPI(title=settings.APP_NAME)

app.add_middleware(
    CORSMiddleware, allow_origins=settings.CORS_ORIGIN,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Server demo client
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/health")
def health():
    return {"status":"ok", "app":settings.APP_NAME}


@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    username = await require_query_params(ws, "username")
    room = ws.query_params.get("room", "lobby")
    
    conn = WSConnection(ws, username=username, room=room)
    await manager.connect(conn)
    
    # Announce Join
    await manager.broadcast(room, WSOutMessage(type="system",
                                               sender="system",
                                               text=f"{username} joined",
                                               room = room).dict())
    
    try:
        while True:
            raw = await ws.receive_json()
            msg = WSInMessage(**raw)
            payload = WSOutMessage(
                type="chat", sender=username, text=msg.text, room=room
            ).dict()
            await manager.broadcast(room, payload)
    
    except WebSocketDisconnect:
        log.info("client disconnected username=%s room=%s", username, room)
    finally:
        await manager.disconnect(conn)
        await manager.broadcast(room, WSOutMessage(type="system",
                                               sender="system",
                                               text=f"{username} joined",
                                               room = room).dict())
