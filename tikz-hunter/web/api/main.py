import os
import asyncio
import json
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Query
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
from psycopg2.extras import RealDictCursor
import grpc
from google.protobuf.json_format import MessageToJson

# It's better to generate these files from the proto definition
# For now, let's assume they are in a reachable path.
# In the Dockerfile, we'll compile them into the root directory.
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from proto import a2a_pb2, a2a_pb2_grpc

# --- FastAPI App Initialization ---
app = FastAPI(title="TikZ-Hunter API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allows the React UI to connect
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Database Connection ---
DATABASE_URL = os.getenv("DATABASE_URL")

def get_db_connection():
    return psycopg2.connect(DATABASE_URL)

# --- gRPC Client Setup ---
BROKER_ADDRESS = os.getenv("BROKER_ADDRESS")

# --- WebSocket Connection Manager ---
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

# --- API Endpoints ---
@app.get("/api/snippets")
async def get_snippets(page: int = 1, limit: int = 20):
    """
    Retrieves paginated snippets from the database.
    """
    offset = (page - 1) * limit
    try:
        conn = get_db_connection()
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                "SELECT uid, hash, snippet, status, source_url, created_at FROM tikz_snippets ORDER BY created_at DESC LIMIT %s OFFSET %s",
                (limit, offset)
            )
            snippets = cur.fetchall()
        conn.close()
        return snippets
    except Exception as e:
        return {"error": str(e)}, 500

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint that streams new snippets from the gRPC broker.
    """
    await manager.connect(websocket)
    try:
        while True:
            # This is a simple keep-alive. The real work is in the gRPC listener.
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        print("Client disconnected from WebSocket.")

async def listen_for_snippets():
    """
    Connects to the gRPC broker and listens for new validated snippets,
    then broadcasts them to all connected WebSocket clients.
    """
    print("Starting gRPC snippet listener...")
    while True:
        try:
            async with grpc.aio.insecure_channel(BROKER_ADDRESS) as channel:
                stub = a2a_pb2_grpc.A2ABrokerStub(channel)
                stream_request = a2a_pb2.StreamRequest(client_id="fastapi-server")
                
                async for snippet in stub.StreamValidatedSnippets(stream_request):
                    print(f"Received snippet from broker stream: {snippet.hash[:8]}")
                    # Convert protobuf message to JSON string for broadcasting
                    snippet_json = MessageToJson(snippet)
                    await manager.broadcast(snippet_json)

        except grpc.aio.AioRpcError as e:
            print(f"gRPC stream error: {e}. Reconnecting in 5 seconds...")
            await asyncio.sleep(5)
        except Exception as e:
            print(f"An unexpected error in gRPC listener: {e}. Reconnecting in 10 seconds...")
            await asyncio.sleep(10)

@app.on_event("startup")
async def startup_event():
    # Start the gRPC listener in the background
    asyncio.create_task(listen_for_snippets())

# To run this: uvicorn tikz-hunter.web.api.main:app --reload