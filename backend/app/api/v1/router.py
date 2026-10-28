from fastapi import APIRouter

from app.api.v1.auth import router as auth_router
from app.api.v1.dashboard import router as dashboard_router
from app.api.v1.catalog import router as catalog_router
from app.api.v1.providers import router as providers_router
from app.api.v1.customers import router as customers_router
from app.api.v1.bookings import router as bookings_router, customer_bookings_router, payments_admin_router
from app.api.v1.support import router as support_router
from app.api.v1.reports import router as reports_router
from app.api.v1.security import router as security_router
from app.api.v1.admins import router as admins_router
from app.api.v1.services import router as services_router
from app.api.v1.provider_onboarding import router as provider_onboarding_router
from app.api.v1.admin_providers import router as admin_providers_router
from app.api.v1.emails import router as emails_router
from app.api.v1.kafka_admin import router as kafka_admin_router
from app.api.v1.ai_support import router as ai_support_router
from app.api.v1.combined_bookings import router as combined_bookings_router
from app.api.v1.oauth import router as oauth_router
from app.api.v1.admin_notifications import router as admin_notifications_router


api_v1_router = APIRouter(prefix="/api/v1")

for r in [
    auth_router,
    dashboard_router,
    catalog_router,
    services_router,
    providers_router,
    admin_providers_router,
    provider_onboarding_router,
    customers_router,
    admins_router,
    bookings_router,
    payments_admin_router,
    customer_bookings_router,
    support_router,
    reports_router,
    security_router,
    emails_router,
    kafka_admin_router,
    ai_support_router,
    combined_bookings_router,
    oauth_router,
    admin_notifications_router,
]:
    api_v1_router.include_router(r)
