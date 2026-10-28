import os
import re
import logging
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, List
from datetime import datetime, timezone

from app.core.config import settings

logger = logging.getLogger("smartserve.services.whatsapp")

# In-memory test outbox for automated tests and local verification without external credentials
_in_memory_whatsapp_outbox: List[Dict[str, Any]] = []


def get_sent_test_whatsapp_messages() -> List[Dict[str, Any]]:
    """Retrieve in-memory WhatsApp messages for test verification."""
    return list(_in_memory_whatsapp_outbox)


def clear_sent_test_whatsapp_messages() -> None:
    """Clear in-memory WhatsApp test outbox."""
    _in_memory_whatsapp_outbox.clear()


class WhatsAppDeliveryResult:
    def __init__(
        self,
        success: bool,
        status: str,  # "Sent", "Delivered", "Unconfigured", "Failed"
        provider_message_id: Optional[str] = None,
        error_message: Optional[str] = None,
    ):
        self.success = success
        self.status = status
        self.provider_message_id = provider_message_id
        self.error_message = error_message

    def to_dict(self) -> Dict[str, Any]:
        return {
            "success": self.success,
            "status": self.status,
            "provider_message_id": self.provider_message_id,
            "error_message": self.error_message,
        }


def validate_and_normalize_phone(phone: Optional[str]) -> Optional[str]:
    """
    Validate and normalize phone number into standard international format.
    Accepts E.164 formats (+91..., +1...) and common national formats.
    Returns None if missing, blank, or invalid.
    """
    if not phone or not str(phone).strip():
        return None
    cleaned = re.sub(r"[\s\-\(\)]", "", str(phone).strip())
    if not cleaned:
        return None
    # If 10-digit national Indian number without prefix, prepend +91
    if re.match(r"^[6-9]\d{9}$", cleaned):
        return f"+91{cleaned}"
    # Standard E.164: + followed by 10 to 15 digits
    if re.match(r"^\+\d{10,15}$", cleaned):
        return cleaned
    return None


class WhatsAppAdapter(ABC):
    @abstractmethod
    def send_notification(
        self,
        recipient_phone: str,
        event_type: str,
        template_name: str,
        parameters: Dict[str, Any],
        fallback_text: str,
    ) -> WhatsAppDeliveryResult:
        """Deliver WhatsApp notification message to a validated recipient phone."""
        pass


class MockInMemoryWhatsAppAdapter(WhatsAppAdapter):
    """
    In-memory mock adapter for local testing and CI/CD pipelines.
    Guarantees no real network transmissions occur and maintains an inspectable outbox.
    """
    def send_notification(
        self,
        recipient_phone: str,
        event_type: str,
        template_name: str,
        parameters: Dict[str, Any],
        fallback_text: str,
    ) -> WhatsAppDeliveryResult:
        msg_id = f"mock-wa-{datetime.now(timezone.utc).timestamp()}"
        record = {
            "recipient_phone": recipient_phone,
            "event_type": event_type,
            "template_name": template_name,
            "parameters": parameters,
            "body": fallback_text,
            "provider_message_id": msg_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        _in_memory_whatsapp_outbox.append(record)
        logger.info("Delivered WhatsApp notification via in-memory mock to %s", recipient_phone)
        return WhatsAppDeliveryResult(
            success=True,
            status="Sent",
            provider_message_id=msg_id,
            error_message=None,
        )


class UnconfiguredWhatsAppAdapter(WhatsAppAdapter):
    """
    Adapter used when WhatsApp Business API credentials are not provided.
    Does NOT claim delivery was successful; records explicit Unconfigured status.
    """
    def send_notification(
        self,
        recipient_phone: str,
        event_type: str,
        template_name: str,
        parameters: Dict[str, Any],
        fallback_text: str,
    ) -> WhatsAppDeliveryResult:
        logger.info(
            "WhatsApp Business API is not configured in this environment. Delivery skipped for %s",
            recipient_phone,
        )
        return WhatsAppDeliveryResult(
            success=False,
            status="Unconfigured",
            provider_message_id=None,
            error_message="WhatsApp provider is unconfigured in this environment. Live delivery disabled.",
        )


class MetaWhatsAppBusinessAdapter(WhatsAppAdapter):
    """
    Official Meta / WhatsApp Cloud Business API implementation.
    Requires WHATSAPP_ACCESS_TOKEN and WHATSAPP_PHONE_NUMBER_ID.
    """
    def __init__(self, phone_number_id: str, access_token: str, api_url: Optional[str] = None):
        self.phone_number_id = phone_number_id
        self.access_token = access_token
        self.api_url = (api_url or "https://graph.facebook.com/v18.0").rstrip("/")

    def send_notification(
        self,
        recipient_phone: str,
        event_type: str,
        template_name: str,
        parameters: Dict[str, Any],
        fallback_text: str,
    ) -> WhatsAppDeliveryResult:
        import requests
        url = f"{self.api_url}/{self.phone_number_id}/messages"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }
        # Format recipient (digits only without + for Meta API)
        to_number = recipient_phone.lstrip("+")
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": to_number,
            "type": "text",
            "text": {"preview_url": False, "body": fallback_text},
        }

        try:
            resp = requests.post(url, json=payload, headers=headers, timeout=10)
            if resp.status_code in (200, 201):
                res_data = resp.json()
                msg_id = None
                messages = res_data.get("messages", [])
                if messages and isinstance(messages, list):
                    msg_id = messages[0].get("id")
                return WhatsAppDeliveryResult(
                    success=True,
                    status="Sent",
                    provider_message_id=msg_id or "meta-wa-sent",
                )
            else:
                err_text = resp.text[:300]
                logger.error("Meta WhatsApp Cloud API error: %d - %s", resp.status_code, err_text)
                return WhatsAppDeliveryResult(
                    success=False,
                    status="Failed",
                    error_message=f"WhatsApp provider API returned status {resp.status_code}",
                )
        except Exception as exc:
            logger.error("Meta WhatsApp Cloud API connection error: %s", type(exc).__name__)
            return WhatsAppDeliveryResult(
                success=False,
                status="Failed",
                error_message="WhatsApp connection timeout or network failure",
            )


def get_whatsapp_adapter() -> WhatsAppAdapter:
    """
    Factory function resolving configured WhatsApp adapter based on environment.
    Defaults to MockInMemoryWhatsAppAdapter if WHATSAPP_BACKEND == 'memory' or in tests.
    """
    backend = getattr(settings, "WHATSAPP_BACKEND", None)
    if not backend:
        backend = os.getenv("WHATSAPP_BACKEND", "memory" if os.getenv("TESTING") or os.getenv("PYTEST_CURRENT_TEST") else "unconfigured")

    backend = backend.lower().strip()
    if backend == "memory":
        return MockInMemoryWhatsAppAdapter()
    elif backend in ("meta", "cloud_api", "whatsapp_cloud"):
        token = getattr(settings, "WHATSAPP_ACCESS_TOKEN", None) or os.getenv("WHATSAPP_ACCESS_TOKEN", "")
        phone_id = getattr(settings, "WHATSAPP_PHONE_NUMBER_ID", None) or os.getenv("WHATSAPP_PHONE_NUMBER_ID", "")
        if token and phone_id:
            api_url = getattr(settings, "WHATSAPP_API_URL", None) or os.getenv("WHATSAPP_API_URL")
            return MetaWhatsAppBusinessAdapter(phone_id, token, api_url)
        return UnconfiguredWhatsAppAdapter()
    else:
        # Default when unconfigured or none
        return UnconfiguredWhatsAppAdapter()
