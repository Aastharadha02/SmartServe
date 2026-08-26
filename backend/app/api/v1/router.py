from fastapi import APIRouter

from app.api.v1.auth import router as auth_router
from app.api.v1.dashboard import router as dashboard_router
from app.api.v1.catalog import router as catalog_router
from app.api.v1.providers import router as providers_router
from app.api.v1.customers import router as customers_router
from app.api.v1.admins import router as admins_router
from app.api.v1.bookings import router as bookings_router
from app.api.v1.support import router as support_router
from app.api.v1.reports import router as reports_router
from app.api.v1.security import router as security_router

api_v1_router = APIRouter(prefix="/api/v1")

for r in [
    auth_router,
    dashboard_router,
    catalog_router,
    providers_router,
    customers_router,
    admins_router,
    bookings_router,
    support_router,
    reports_router,
    security_router
]:
    api_v1_router.include_router(r)
