import os
from pydantic_settings import BaseSettings
from pydantic import field_validator
from typing import List, Union, Any
from dotenv import load_dotenv

_backend_env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), ".env")
if os.path.exists(_backend_env_path):
    load_dotenv(_backend_env_path)
else:
    load_dotenv()


class Settings(BaseSettings):
    APP_NAME: str = "SmartServe"
    API_V1_PREFIX: str = "/api/v1"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "dev")
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg2://postgres:postgres@localhost:5432/smartserve",
    )
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", os.getenv("JWT_SECRET", "change-me-smartserve-secret-key-32chars"))
    JWT_SECRET: str = os.getenv("JWT_SECRET_KEY", os.getenv("JWT_SECRET", "change-me-smartserve-secret-key-32chars"))
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1 day
    CORS_ORIGINS: Union[List[str], str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
        "http://localhost:5175",
        "http://127.0.0.1:5175",
        "http://localhost:5176",
        "http://127.0.0.1:5176",
    ]

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Any) -> List[str]:
        default_origins = [
            "http://localhost:5173",
            "http://localhost:3000",
            "http://127.0.0.1:5173",
            "http://localhost:5174",
            "http://127.0.0.1:5174",
            "http://localhost:5175",
            "http://127.0.0.1:5175",
            "http://localhost:5176",
            "http://127.0.0.1:5176",
        ]
        if v is None:
            return default_origins
        if isinstance(v, str):
            raw = v.strip()
            if not raw:
                return default_origins
            if raw.startswith("[") and raw.endswith("]"):
                try:
                    import json
                    parsed = [str(x).strip().rstrip("/") for x in json.loads(raw) if str(x).strip()]
                except Exception:
                    parsed = [x.strip().rstrip("/") for x in raw.strip("[]").split(",") if x.strip()]
            else:
                parsed = [x.strip().rstrip("/") for x in raw.split(",") if x.strip()]
            combined = list(default_origins)
            for origin in parsed:
                if origin and origin not in combined:
                    combined.append(origin)
            return combined
        elif isinstance(v, (list, tuple)):
            combined = list(default_origins)
            for item in v:
                clean = str(item).strip().rstrip("/")
                if clean and clean not in combined:
                    combined.append(clean)
            return combined
        return default_origins

    KAFKA_BOOTSTRAP_SERVERS: str = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
    KAFKA_CONSUMER_GROUP: str = os.getenv("KAFKA_CONSUMER_GROUP", "smartserve-backend-group")
    KAFKA_ENABLED: bool = os.getenv("KAFKA_ENABLED", "true").lower() in ("true", "1", "yes")
    KAFKA_SECURITY_PROTOCOL: str = os.getenv("KAFKA_SECURITY_PROTOCOL", "PLAINTEXT")
    KAFKA_SASL_MECHANISM: str = os.getenv("KAFKA_SASL_MECHANISM", "PLAIN")
    KAFKA_SASL_USERNAME: str = os.getenv("KAFKA_SASL_USERNAME", "")
    KAFKA_SASL_PASSWORD: str = os.getenv("KAFKA_SASL_PASSWORD", "")

    # AI Support Configuration
    MAX_AI_SUPPORT_MESSAGES: int = int(os.getenv("MAX_AI_SUPPORT_MESSAGES", "5"))
    OPENROUTER_API_KEY: str = os.getenv("OPENROUTER_API_KEY", "")
    OPENROUTER_MODEL: str = os.getenv("OPENROUTER_MODEL", "openrouter/free")

    # OAuth / Social Login Configuration
    GOOGLE_CLIENT_ID: str = os.getenv("GOOGLE_CLIENT_ID", "")
    GOOGLE_CLIENT_SECRET: str = os.getenv("GOOGLE_CLIENT_SECRET", "")
    GOOGLE_REDIRECT_URI: str = os.getenv("GOOGLE_REDIRECT_URI", "http://localhost:5174/auth/callback/google")

    APPLE_CLIENT_ID: str = os.getenv("APPLE_CLIENT_ID", "")
    APPLE_CLIENT_SECRET: str = os.getenv("APPLE_CLIENT_SECRET", "")
    APPLE_REDIRECT_URI: str = os.getenv("APPLE_REDIRECT_URI", "http://localhost:5174/auth/callback/apple")

    GITHUB_CLIENT_ID: str = os.getenv("GITHUB_CLIENT_ID", "")
    GITHUB_CLIENT_SECRET: str = os.getenv("GITHUB_CLIENT_SECRET", "")
    GITHUB_REDIRECT_URI: str = os.getenv("GITHUB_REDIRECT_URI", "http://localhost:5174/auth/callback/github")

    # Email & SMTP Configuration
    SMTP_HOST: str = os.getenv("SMTP_HOST", "")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USER: str = os.getenv("SMTP_USER", "")
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD", "")
    SMTP_USE_TLS: bool = os.getenv("SMTP_USE_TLS", "true").lower() in ("true", "1", "yes")
    SMTP_USE_SSL: bool = os.getenv("SMTP_USE_SSL", "false").lower() in ("true", "1", "yes")
    SMTP_FROM_EMAIL: str = os.getenv("SMTP_FROM_EMAIL", "noreply@smartserve.com")
    SMTP_TIMEOUT_SECONDS: int = int(os.getenv("SMTP_TIMEOUT_SECONDS", "10"))
    EMAIL_BACKEND: str = os.getenv("EMAIL_BACKEND", "memory")  # "smtp" or "memory" (test adapter)
    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://localhost:5174")

    # WhatsApp Business API Configuration
    WHATSAPP_BACKEND: str = os.getenv("WHATSAPP_BACKEND", "memory")  # "memory", "meta", "unconfigured"
    WHATSAPP_PHONE_NUMBER_ID: str = os.getenv("WHATSAPP_PHONE_NUMBER_ID", "")
    WHATSAPP_ACCESS_TOKEN: str = os.getenv("WHATSAPP_ACCESS_TOKEN", "")
    WHATSAPP_BUSINESS_ACCOUNT_ID: str = os.getenv("WHATSAPP_BUSINESS_ACCOUNT_ID", "")
    WHATSAPP_API_URL: str = os.getenv("WHATSAPP_API_URL", "https://graph.facebook.com/v18.0")
    WHATSAPP_ENABLED: bool = os.getenv("WHATSAPP_ENABLED", "false").lower() in ("true", "1", "yes")

    # Antivirus & Upload Malware Scanning (ClamAV)
    CLAMAV_ENABLED: bool = os.getenv("CLAMAV_ENABLED", "false").lower() in ("true", "1", "yes")
    CLAMAV_HOST: str = os.getenv("CLAMAV_HOST", "localhost")
    CLAMAV_PORT: int = int(os.getenv("CLAMAV_PORT", "3310"))
    CLAMAV_TIMEOUT_SECONDS: int = int(os.getenv("CLAMAV_TIMEOUT_SECONDS", "5"))
    CLAMAV_OPTIONAL_IN_DEV: bool = os.getenv("CLAMAV_OPTIONAL_IN_DEV", "true").lower() in ("true", "1", "yes")

    class Config:
        case_sensitive = True
        env_file = ".env"
        extra = "ignore"



settings = Settings()
