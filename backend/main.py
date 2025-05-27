from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from auth import router as auth_router
from db import init_db
from ws import manager 
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
app.include_router(auth_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def startup_event():
    try:
        await init_db()
        logger.info("Application started successfully")
    except Exception as e:
        logger.error(f"Failed to start application: {e}")
        raise

async def shutdown_event():
    # Add any shutdown cleanup here if needed
    pass

@app.router.lifespan_context
async def lifespan(app: FastAPI):
    await startup_event()
    yield
    await shutdown_event()

@app.get("/")
async def root():
    return {"message": "API is working"}

@app.websocket("/ws/{username}")
async def websocket_endpoint(websocket: WebSocket, username: str):
    await manager.connect(username, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(username, data)
    except WebSocketDisconnect:
        manager.disconnect(username)
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        manager.disconnect(username)