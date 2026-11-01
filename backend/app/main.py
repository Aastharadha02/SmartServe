import time
import logging
import threading
import traceback
from collections import defaultdict
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.core.database import Base, engine
from app.api.v1.router import api_v1_router
from app.api.v1.customer import router as customer_router
from app.api.v1.ai_support import router as ai_support_router
from app.api.v1.ws import router as ws_router
from app.services.kafka import kafka_producer, kafka_consumer

logger = logging.getLogger("smartserve.api")

# Auto-create tables and initial seeders only in non-production development mode
if settings.ENVIRONMENT != "production":
    try:
        Base.metadata.create_all(bind=engine)
    except Exception:
        pass
    try:
        from app.seed_admins import seed_initial_admins
        seed_initial_admins()
    except Exception:
        pass
    try:
        from app.seed_providers import seed_initial_providers
        seed_initial_providers()
    except Exception:
        pass
    try:
        from app.seed_bookings import seed_operational_bookings
        seed_operational_bookings()
    except Exception:
        pass

import asyncio

async def keep_render_alive():
    """Background keep-alive loop to prevent Render free instance from sleeping."""
    await asyncio.sleep(60)
    while True:
        try:
            import urllib.request
            req = urllib.request.Request(
                "https://smartserve-api-de3f.onrender.com/health",
                headers={"User-Agent": "SmartServe-KeepAlive/1.0"}
            )
            await asyncio.to_thread(urllib.request.urlopen, req, timeout=8)
        except Exception:
            pass
        await asyncio.sleep(480) # Ping every 8 minutes


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Spawn Kafka producer & consumer non-blockingly as background tasks.
    # This ensures Uvicorn immediately begins accepting HTTP connections and serving
    # the /health endpoint without waiting for broker connections on cold boot.
    producer_task = asyncio.create_task(kafka_producer.start())
    consumer_task = asyncio.create_task(kafka_consumer.start())
    keepalive_task = asyncio.create_task(keep_render_alive())
    yield
    # Shutdown: Cleanly cancel pending connection attempts and stop services
    try:
        if not keepalive_task.done():
            keepalive_task.cancel()
    except Exception:
        pass
    try:
        if not producer_task.done():
            producer_task.cancel()
    except Exception:
        pass
    try:
        if not consumer_task.done():
            consumer_task.cancel()
    except Exception:
        pass
    try:
        await kafka_consumer.stop()
    except Exception:
        pass
    try:
        await kafka_producer.stop()
    except Exception:
        pass



app = FastAPI(
    title=settings.APP_NAME,
    description="SmartServe - AI-powered multi-service booking & marketplace API",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)


# =====================================================================
# SECURITY MIDDLEWARE & DEFENSE-IN-DEPTH CONTROLS
# =====================================================================

# 1. Rate Limiting for Authentication Endpoints (Shared Multi-Worker with Memory Fallback)
_rate_limit_records = defaultdict(list)
_rate_limit_lock = threading.Lock()
_RATE_LIMIT_MAX = 30  # Max requests per window
_RATE_LIMIT_WINDOW = 60  # 60 seconds
_SENSITIVE_AUTH_PATHS = {
    "/api/v1/auth/login",
    "/api/v1/auth/signup",
    "/api/v1/auth/register",
    "/api/v1/customer/auth/login",
    "/api/v1/customer/auth/register",
    "/api/v1/customer/auth/forgot-password",
    "/api/v1/customer/auth/reset-password",
    "/api/v1/customer/auth/oauth/google/callback",
    "/api/v1/customer/auth/oauth/apple/callback",
    "/api/v1/customer/auth/oauth/github/callback",
}


def check_shared_rate_limit(key: str, max_requests: int = _RATE_LIMIT_MAX, window_seconds: int = _RATE_LIMIT_WINDOW) -> bool:
    """
    Check rate limit against database (shared across all multi-worker uvicorn processes).
    Falls back gracefully to local memory on transient database errors or testing environments.
    Returns True if request allowed, False if rate limited.
    """
    try:
        from app.core.database import SessionLocal
        from app.models.security import RateLimitEntry
        from datetime import datetime, timezone, timedelta
        import random

        db = SessionLocal()
        try:
            now_dt = datetime.now(timezone.utc)
            window_start = now_dt - timedelta(seconds=window_seconds)

            # Probabilistic cleanup of entries older than 5 minutes (isolated transaction)
            if random.random() < 0.02:
                try:
                    prune_cutoff = now_dt - timedelta(minutes=5)
                    db.query(RateLimitEntry).filter(RateLimitEntry.created_at < prune_cutoff).delete(synchronize_session=False)
                    db.commit()
                except Exception:
                    db.rollback()

            count = db.query(RateLimitEntry).filter(
                RateLimitEntry.key == key,
                RateLimitEntry.created_at >= window_start
            ).count()

            if count >= max_requests:
                return False

            new_entry = RateLimitEntry(key=key, created_at=now_dt)
            db.add(new_entry)
            db.commit()
            return True
        finally:
            db.close()
    except Exception as exc:
        logger.warning("Database unavailable for rate limiting, falling back to process memory sliding window: %s", type(exc).__name__)
        # Fallback to process memory sliding-window: thread-safe, strictly enforces max_requests
        with _rate_limit_lock:
            now = time.time()
            history = [t for t in _rate_limit_records[key] if now - t < window_seconds]
            if len(history) >= max_requests:
                return False
            history.append(now)
            _rate_limit_records[key] = history
            # Bound in-memory cache size if too many keys accumulate during prolonged DB outage
            if len(_rate_limit_records) > 5000:
                keys_to_del = [k for k, v in list(_rate_limit_records.items())[:1000] if not v or (now - v[-1] > window_seconds)]
                for k in keys_to_del:
                    _rate_limit_records.pop(k, None)
            return True


@app.middleware("http")
async def rate_limit_auth_middleware(request: Request, call_next):
    path = request.url.path
    if path in _SENSITIVE_AUTH_PATHS and request.method == "POST":
        client_ip = (
            request.headers.get("x-forwarded-for")
            or (request.client.host if request.client else "127.0.0.1")
        ).split(",")[0].strip()
        key = f"{client_ip}:{path}"

        allowed = check_shared_rate_limit(key)
        if not allowed:
            return JSONResponse(
                status_code=429,
                content={"detail": "Too many authentication attempts. Please try again after 60 seconds."},
                headers={"Retry-After": "60"}
            )

    return await call_next(request)



# 2. Security Headers Injection Middleware
@app.middleware("http")
async def add_security_headers_middleware(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "img-src 'self' data: https:; "
        "script-src 'self' 'unsafe-inline'; "
        "style-src 'self' 'unsafe-inline'; "
        "font-src 'self' data: https:; "
        "connect-src 'self' ws: wss: http: https:; "
        "frame-ancestors 'none';"
    )
    if settings.ENVIRONMENT == "production":
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    return response


# 3. Validation Exception Handler
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for err in exc.errors():
        field = ".".join(str(loc) for loc in err.get("loc", []) if loc != "body")
        msg = err.get("msg", "Invalid value")
        errors.append(f"{field}: {msg}" if field else msg)
    detail_str = "; ".join(errors)
    return JSONResponse(
        status_code=422,
        content={"detail": detail_str, "errors": exc.errors()}
    )


# 4. Global Unhandled Exception Handler (Information Disclosure Prevention)
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    err_msg = f"[UnhandledException] {request.method} {request.url.path}: {exc}\n{traceback.format_exc()}"
    print(err_msg, flush=True)
    logger.error(err_msg)
    return JSONResponse(
        status_code=500,
        content={"detail": "An internal server error occurred. Our engineering operations team has been notified."}
    )



# 5. CORS Configuration (Restricted in production, flexible in development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_origin_regex=r"^https?://([a-zA-Z0-9_-]+\.)*vercel\.app(:[0-9]+)?$|^https?://(localhost|127\.0\.0\.1|192\.168\.[0-9]+\.[0-9]+|172\.[0-9]+\.[0-9]+\.[0-9]+|10\.[0-9]+\.[0-9]+\.[0-9]+)(:[0-9]+)?$",
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)


# Mount API Routers
app.include_router(api_v1_router)
app.include_router(customer_router, prefix=settings.API_V1_PREFIX)
app.include_router(ai_support_router)
app.include_router(ws_router)
app.include_router(ws_router, prefix=settings.API_V1_PREFIX)


# Mount Static Files for Uploads
import os
from fastapi.staticfiles import StaticFiles
os.makedirs("customer_uploads", exist_ok=True)
app.mount("/static/uploads", StaticFiles(directory="customer_uploads"), name="static_uploads")


# System Endpoints (Sanitized to prevent connection-string credential leaks)
@app.get("/health", tags=["System"])
@app.get("/api/v1/health", tags=["System"])
def health_check():
    """Sanitized health check endpoint: reports status without disclosing database credentials."""
    return {
        "status": "healthy",
        "service": settings.APP_NAME,
        "environment": settings.ENVIRONMENT,
        "database": "connected" if engine else "disconnected",
    }


@app.get("/", tags=["System"])
def root():
    return {
        "message": "Welcome to SmartServe API",
        "docs": "/docs",
        "version": "0.1.0",
    }
