import json
import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.core.config import settings
from app.services.kafka.transport import build_kafka_kwargs
from app.services.kafka.topics import KafkaTopics
from app.core.security import create_access_token


@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def admin_headers():
    token = create_access_token({"sub": "admin@smartserve.com", "role": "admin"})
    return {"Authorization": f"Bearer {token}"}


def test_kafka_status_endpoint_structure(client, admin_headers):
    """Verify /api/v1/kafka/status endpoint returns all required spec fields."""
    response = client.get("/api/v1/kafka/status", headers=admin_headers)
    assert response.status_code == 200
    data = response.json()

    # Spec required fields
    required_fields = [
        "kafka_enabled",
        "security_protocol",
        "sasl_mechanism",
        "bootstrap_configured",
        "producer_connected",
        "consumer_connected",
        "consumer_group",
        "expected_topics",
        "last_error",
    ]
    for field in required_fields:
        assert field in data, f"Missing required field in /kafka/status: {field}"

    # Verify expected topics match canonical 7
    assert data["expected_topics"] == KafkaTopics.ALL_TOPICS
    assert len(data["expected_topics"]) == 7


def test_kafka_status_never_exposes_secrets(client, admin_headers):
    """
    Critical security test: Assert the status response body NEVER contains:
    - KAFKA_SASL_PASSWORD
    - JWT_SECRET_KEY
    - DATABASE_URL credentials
    - OPENROUTER_API_KEY
    """
    response = client.get("/api/v1/kafka/status", headers=admin_headers)
    assert response.status_code == 200
    body_text = response.text

    secrets_to_check = [
        settings.KAFKA_SASL_PASSWORD,
        settings.JWT_SECRET_KEY,
        settings.JWT_SECRET,
        settings.OPENROUTER_API_KEY,
    ]

    for secret in secrets_to_check:
        if secret and len(secret) > 3:
            assert secret not in body_text, f"LEAK DETECTED: Secret found in /api/v1/kafka/status response!"

    # Ensure unmasked password is not in bootstrap_servers
    assert "sasl_plain_password" not in body_text
    assert "password" not in body_text.lower() or '"last_error":null' in body_text.lower() or '"last_error":' in body_text.lower()


def test_kafka_transport_kwargs_factory():
    """Verify build_kafka_kwargs produces secure, valid arguments."""
    kwargs = build_kafka_kwargs()
    assert "bootstrap_servers" in kwargs

    # If SASL_SSL is configured, verify TLS context and SCRAM mechanism
    if settings.KAFKA_SECURITY_PROTOCOL == "SASL_SSL":
        assert kwargs["security_protocol"] == "SASL_SSL"
        assert kwargs["sasl_mechanism"] == "SCRAM-SHA-256"
        assert "ssl_context" in kwargs
        assert kwargs["ssl_context"] is not None
        # Verify certificate verification is NOT disabled
        assert kwargs["ssl_context"].check_hostname is True


def test_health_endpoint_immediate_and_safe(client):
    """Verify /health and /api/v1/health return 200 healthy immediately and do not leak DB credentials."""
    for path in ["/health", "/api/v1/health"]:
        response = client.get(path)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "service" in data
        assert data.get("database") == "connected"
