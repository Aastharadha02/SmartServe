from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.core.websockets import ws_manager

router = APIRouter(prefix="/ws", tags=["Real-time WebSockets Stream"])

@router.websocket("/dashboard")
async def websocket_dashboard_stream(websocket: WebSocket):
    """Real-time WebSocket connection for live Operations Dashboard updates."""
    await ws_manager.connect(websocket, "dashboard")
    try:
        while True:
            # Keep connection active and receive messages
            data = await websocket.receive_text()
            await websocket.send_json({"type": "pong", "message": "Dashboard stream active"})
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket, "dashboard")

@router.websocket("/emergency-alerts")
async def websocket_emergency_stream(websocket: WebSocket):
    """Real-time WebSocket connection for emergency request notifications."""
    await ws_manager.connect(websocket, "emergency")
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_json({"type": "pong", "message": "Emergency alert stream active"})
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket, "emergency")

@router.websocket("/bookings/{booking_id}")
async def websocket_booking_stream(websocket: WebSocket, booking_id: str):
    """Real-time WebSocket connection for live booking tracking."""
    channel = f"booking_{booking_id}"
    await ws_manager.connect(websocket, channel)
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_json({"type": "pong", "booking_id": booking_id, "status": "tracking_active"})
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket, channel)
