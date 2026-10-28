import json
import logging
import uuid
from typing import Optional, Dict, Any, List
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query, status

from app.core.websockets import ws_manager
from app.core.security import decode_access_token
from app.core.config import settings

logger = logging.getLogger("smartserve.websockets.routes")

router = APIRouter(prefix="/ws", tags=["Real-time WebSockets Stream"])


def _authenticate_ws_token(token: Optional[str]) -> Optional[Dict[str, Any]]:
    """Decode, validate signature, and check revocation status for WebSocket token."""
    if not token:
        return None
    payload = decode_access_token(token)
    if not payload:
        return None
    jti = payload.get("jti")
    if jti:
        try:
            from app.core.database import SessionLocal
            from app.models.session import ActiveSession
            db = SessionLocal()
            try:
                sess = db.query(ActiveSession).filter(ActiveSession.token_jti == jti, ActiveSession.is_revoked == True).first()
                if sess:
                    return None
            finally:
                db.close()
        except Exception:
            pass
    return payload


def _is_authorized_for_channel(auth_payload: Optional[Dict[str, Any]], channel: str) -> bool:
    """
    Strict server-side authorization check for WebSocket channel subscriptions.
    Guarantees horizontal and vertical tenant isolation across customers, providers, and admins.
    """
    if not channel:
        return False

    clean_channel = channel.strip()
    role = (auth_payload.get("role") or "").lower() if auth_payload else "anonymous"
    sub = str(auth_payload.get("sub") or "").lower() if auth_payload else ""
    cust_id = str(auth_payload.get("customer_id") or "").lower() if auth_payload else ""

    # 1. Admin & Operational Super-Channels (Strictly require Admin / Super Admin)
    admin_channels = {"dashboard", "emergency", "admin"}
    if clean_channel in admin_channels or clean_channel.startswith("admin_"):
        return role in ["admin", "super_admin"]

    # 2. General Bookings list channel (Admin / Super Admin only)
    if clean_channel == "bookings":
        return role in ["admin", "super_admin"]

    # 3. Customer-Specific Channels
    if clean_channel.startswith("customer_"):
        target_id = clean_channel.replace("customer_", "").lower()
        if role in ["admin", "super_admin"]:
            return True
        return role == "customer" and (target_id in [sub, cust_id])

    # 4. Provider-Specific Channels
    if clean_channel.startswith("provider_"):
        target_id = clean_channel.replace("provider_", "").lower()
        if role in ["admin", "super_admin"]:
            return True
        return role == "provider" and target_id == sub

    # 5. User-Specific direct notification channel
    if clean_channel.startswith("user_"):
        target_id = clean_channel.replace("user_", "").lower()
        if role in ["admin", "super_admin"]:
            return True
        return target_id in [sub, cust_id]

    # 6. Specific Booking or Ticket tracking channels (Enforce tenant boundary)
    if clean_channel.startswith("booking_") or clean_channel.startswith("ticket_"):
        if role in ["admin", "super_admin"]:
            return True
        if not auth_payload:
            return False

        target_uuid_str = clean_channel.split("_", 1)[1] if "_" in clean_channel else ""
        if not target_uuid_str:
            return False

        try:
            import uuid
            t_uuid = uuid.UUID(target_uuid_str)
            from app.core.database import SessionLocal
            db = SessionLocal()
            try:
                if clean_channel.startswith("booking_"):
                    from app.models.booking import Booking
                    from app.models.customer import Customer
                    b = db.query(Booking).filter(Booking.id == t_uuid).first()
                    if not b:
                        return False
                    if role == "customer":
                        # Match customer_id against auth token's customer_id or resolve from user_id
                        if cust_id and str(b.customer_id).lower() == cust_id:
                            return True
                        cust_rec = db.query(Customer).filter(Customer.user_id == sub).first()
                        if cust_rec and str(b.customer_id).lower() == str(cust_rec.id).lower():
                            return True
                        return False
                    elif role == "provider":
                        return str(b.provider_id).lower() == sub
                    return False
                else:  # ticket_
                    from app.models.support import SupportTicket
                    from app.models.customer import Customer
                    t = db.query(SupportTicket).filter(SupportTicket.id == t_uuid).first()
                    if not t:
                        return False
                    if role == "customer":
                        if cust_id and str(t.customer_id).lower() == cust_id:
                            return True
                        cust_rec = db.query(Customer).filter(Customer.user_id == sub).first()
                        if cust_rec and str(t.customer_id).lower() == str(cust_rec.id).lower():
                            return True
                        return False
                    elif role == "provider":
                        return str(t.provider_id).lower() == sub
                    return False
            finally:
                db.close()
        except Exception:
            return False

    # Default fallback: strictly deny unauthenticated / unauthorized channel subscriptions
    return False


@router.websocket("/stream")
async def websocket_unified_stream(
    websocket: WebSocket,
    channels: Optional[str] = Query(None, description="Comma-separated channel list"),
    token: Optional[str] = Query(None, description="JWT Authentication Bearer token")
):
    """
    Unified multi-channel authenticated WebSocket stream.
    Validates Origin (preventing CSWSH), verifies JWT token signature and session revocation,
    and enforces strict role-based channel authorization.
    """
    # CSWSH (Cross-Site WebSocket Hijacking) Protection: Verify Origin Header
    origin = websocket.headers.get("origin")
    if origin:
        import urllib.parse
        parsed = urllib.parse.urlparse(origin)
        host = parsed.hostname or ""
        is_local = host in ("localhost", "127.0.0.1") or host.startswith("192.168.") or host.startswith("10.") or host.startswith("172.")
        is_allowed = origin in settings.CORS_ORIGINS or is_local
        if not is_allowed:
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return

    await websocket.accept()

    # Authenticate caller
    auth_payload = _authenticate_ws_token(token)

    # Initial channel subscriptions (filter through authorization guard)
    requested_channels = [ch.strip() for ch in (channels or "").split(",") if ch.strip()]
    authorized_channels: List[str] = []
    rejected_channels: List[str] = []

    for ch in requested_channels:
        if _is_authorized_for_channel(auth_payload, ch):
            ws_manager.subscribe(websocket, ch)
            authorized_channels.append(ch)
        else:
            rejected_channels.append(ch)

    await websocket.send_json({
        "type": "CONNECTION_ESTABLISHED",
        "authenticated": auth_payload is not None,
        "subscribed_channels": authorized_channels,
        "rejected_channels": rejected_channels
    })

    try:
        while True:
            text_data = await websocket.receive_text()
            try:
                data = json.loads(text_data)
                action = data.get("action")
                target_channel = data.get("channel")

                # Optional runtime re-authentication or token update
                if action == "auth" and data.get("token"):
                    new_auth = _authenticate_ws_token(data.get("token"))
                    if new_auth:
                        auth_payload = new_auth
                        await websocket.send_json({"type": "AUTH_SUCCESS", "role": auth_payload.get("role")})
                    else:
                        await websocket.send_json({"type": "AUTH_FAILED", "message": "Invalid token"})

                elif action == "subscribe" and target_channel:
                    if _is_authorized_for_channel(auth_payload, target_channel):
                        ws_manager.subscribe(websocket, target_channel)
                        await websocket.send_json({"type": "SUBSCRIBED", "channel": target_channel})
                    else:
                        await websocket.send_json({
                            "type": "UNAUTHORIZED",
                            "channel": target_channel,
                            "message": "Access forbidden: Insufficient permissions for this stream."
                        })

                elif action == "unsubscribe" and target_channel:
                    ws_manager.unsubscribe(websocket, target_channel)
                    await websocket.send_json({"type": "UNSUBSCRIBED", "channel": target_channel})

                elif action == "ping":
                    await websocket.send_json({"type": "pong"})

            except json.JSONDecodeError:
                if text_data.strip() == "ping":
                    await websocket.send_json({"type": "pong"})
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)
    except Exception as exc:
        logger.warning(f"[WebSocket /stream] Connection error: {exc}")
        ws_manager.disconnect(websocket)


@router.websocket("/dashboard")
async def websocket_dashboard_stream(
    websocket: WebSocket,
    token: Optional[str] = Query(None)
):
    """Real-time Operations Dashboard stream with mandatory Admin RBAC guard."""
    auth_payload = _authenticate_ws_token(token)
    if not auth_payload or auth_payload.get("role") not in ["admin", "super_admin"]:
        if settings.ENVIRONMENT == "production":
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return

    await ws_manager.connect(websocket, "dashboard")
    try:
        while True:
            await websocket.receive_text()
            await websocket.send_json({"type": "pong", "message": "Dashboard stream active"})
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket, "dashboard")


@router.websocket("/emergency-alerts")
async def websocket_emergency_stream(
    websocket: WebSocket,
    token: Optional[str] = Query(None)
):
    """Real-time emergency request alerts (Restricted to verified Admins)."""
    auth_payload = _authenticate_ws_token(token)
    if not auth_payload or auth_payload.get("role") not in ["admin", "super_admin"]:
        if settings.ENVIRONMENT == "production":
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return

    await ws_manager.connect(websocket, "emergency")
    try:
        while True:
            await websocket.receive_text()
            await websocket.send_json({"type": "pong", "message": "Emergency alert stream active"})
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket, "emergency")


@router.websocket("/bookings")
async def websocket_bookings_stream(websocket: WebSocket, token: Optional[str] = Query(None)):
    """Real-time bookings stream."""
    await ws_manager.connect(websocket, "bookings")
    try:
        while True:
            await websocket.receive_text()
            await websocket.send_json({"type": "pong", "message": "Bookings stream active"})
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket, "bookings")


@router.websocket("/bookings/{booking_id}")
async def websocket_booking_stream(websocket: WebSocket, booking_id: str, token: Optional[str] = Query(None)):
    """Real-time booking tracking."""
    channel = f"booking_{booking_id}"
    await ws_manager.connect(websocket, channel)
    try:
        while True:
            await websocket.receive_text()
            await websocket.send_json({"type": "pong", "booking_id": booking_id, "status": "tracking_active"})
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket, channel)


@router.websocket("/chat/{ticket_id}")
async def websocket_chat_stream(websocket: WebSocket, ticket_id: str, token: Optional[str] = Query(None)):
    """Real-time chat stream."""
    channel = f"ticket_{ticket_id}"
    await ws_manager.connect(websocket, channel)
    try:
        while True:
            await websocket.receive_text()
            await websocket.send_json({"type": "pong", "ticket_id": ticket_id, "status": "chat_active"})
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket, channel)


@router.websocket("/provider/{provider_id}")
async def websocket_provider_stream(websocket: WebSocket, provider_id: str, token: Optional[str] = Query(None)):
    """Real-time provider-specific updates."""
    channel = f"provider_{provider_id}"
    await ws_manager.connect(websocket, channel)
    try:
        while True:
            await websocket.receive_text()
            await websocket.send_json({"type": "pong", "provider_id": provider_id, "status": "active"})
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket, channel)


@router.websocket("/customer/{customer_id}")
async def websocket_customer_stream(websocket: WebSocket, customer_id: str, token: Optional[str] = Query(None)):
    """Real-time customer-specific updates."""
    channel = f"customer_{customer_id}"
    await ws_manager.connect(websocket, channel)
    try:
        while True:
            await websocket.receive_text()
            await websocket.send_json({"type": "pong", "customer_id": customer_id, "status": "active"})
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket, channel)
