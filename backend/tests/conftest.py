"""
Pytest configuration and global fixtures for SmartServe backend test suite.
Ensures routine automated tests always use in-memory/mocked test adapters
and never make live outbound connections to SMTP or external third-party services.
"""
import pytest
from app.core.config import settings
from app.services import email_service
from app.services.notification import whatsapp_adapter


@pytest.fixture(autouse=True)
def force_mock_messaging_backends_for_automated_tests(monkeypatch):
    """
    Ensure routine automated tests ALWAYS use the in-memory/mocked email and WhatsApp adapters.
    Prevents tests from attempting outbound SMTP connections or sending real external
    WhatsApp/email messages to generated, simulated, or invalid test addresses.
    """
    monkeypatch.setattr(settings, "EMAIL_BACKEND", "memory")
    monkeypatch.setattr(settings, "WHATSAPP_BACKEND", "memory")
    email_service.clear_sent_test_emails()
    whatsapp_adapter.clear_sent_test_whatsapp_messages()
    yield
    email_service.clear_sent_test_emails()
    whatsapp_adapter.clear_sent_test_whatsapp_messages()
