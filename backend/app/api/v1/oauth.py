import uuid
import re
import secrets
import logging
import urllib.parse
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any

try:
    import requests
except ImportError:
    requests = None

try:
    from jose import jwt
except ImportError:
    import jwt
from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.dependencies import get_db
from app.core.security import hash_password, create_access_token
from app.models.user import User, UserSession
from app.models.customer import Customer
from app.models.oauth import OAuthAccount
from app.schemas.customer_schemas import CustomerTokenResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth/oauth", tags=["OAuth Authentication"])


# --- Schemas ---

class ProviderStatus(BaseModel):
    configured: bool
    name: str

class OAuthProvidersResponse(BaseModel):
    google: ProviderStatus
    apple: ProviderStatus
    github: ProviderStatus

class OAuthAuthorizeResponse(BaseModel):
    provider: str
    authorization_url: str
    state: str

class OAuthCallbackPayload(BaseModel):
    code: str
    state: str
    redirect_uri: Optional[str] = None


# --- Helpers ---

def generate_pkce_pair() -> tuple[str, str]:
    """Generate RFC 7636 PKCE code_verifier and S256 code_challenge."""
    import base64
    import hashlib
    verifier = secrets.token_urlsafe(64)
    digest = hashlib.sha256(verifier.encode('ascii')).digest()
    challenge = base64.urlsafe_b64encode(digest).decode('ascii').rstrip('=')
    return verifier, challenge


def is_allowed_redirect_uri(redirect_uri: str) -> bool:
    """Verify that client-provided redirect_uri belongs to an allowed frontend origin."""
    try:
        parsed = urllib.parse.urlparse(redirect_uri)
        if not (parsed.scheme in ("http", "https") and parsed.netloc):
            return False
        origin = f"{parsed.scheme}://{parsed.netloc}"
        if origin in settings.CORS_ORIGINS:
            return True
        if parsed.hostname in ("localhost", "127.0.0.1"):
            return True
        return False
    except Exception:
        return False


def generate_oauth_state(provider: str, redirect_uri: Optional[str] = None, code_verifier: Optional[str] = None) -> str:
    """Generate a signed, tamper-proof, 15-minute expiring state parameter with anti-replay nonce, bound redirect_uri, and PKCE verifier."""
    payload = {
        "provider": provider,
        "redirect_uri": redirect_uri,
        "code_verifier": code_verifier,
        "nonce": secrets.token_hex(16),
        "exp": datetime.now(timezone.utc) + timedelta(minutes=15),
    }
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def verify_oauth_state(state: str, expected_provider: str) -> bool:
    """Validate the cryptographic state parameter to prevent CSRF."""
    try:
        payload = jwt.decode(state, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        return payload.get("provider") == expected_provider
    except Exception as e:
        logger.warning(f"[OAuth] Invalid state token: {e}")
        return False


def verify_and_consume_oauth_state(state: str, expected_provider: str, db: Session) -> Optional[Dict[str, Any]]:
    """Validate state signature, expiration, provider, and atomically consume nonce to prevent replay attacks."""
    try:
        payload = jwt.decode(state, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        if payload.get("provider") != expected_provider:
            logger.warning("[OAuth] State provider mismatch")
            return None
        nonce = payload.get("nonce")
        if not nonce:
            return None

        from app.models.security import RateLimitEntry
        nonce_key = f"oauth_nonce:{nonce}"
        existing = db.query(RateLimitEntry).filter(RateLimitEntry.key == nonce_key).first()
        if existing:
            logger.warning("[OAuth] State replay detected for nonce: %s", nonce)
            return None

        # Atomically record nonce as consumed
        db.add(RateLimitEntry(key=nonce_key, created_at=datetime.now(timezone.utc)))
        db.commit()
        return payload
    except Exception as e:
        logger.warning(f"[OAuth] Invalid state token: {e}")
        return None


def is_provider_configured(provider: str) -> bool:
    """Check whether local environment variables exist for the provider."""
    p = provider.lower()
    if p == "google":
        return bool(settings.GOOGLE_CLIENT_ID and settings.GOOGLE_CLIENT_SECRET)
    elif p == "apple":
        return bool(settings.APPLE_CLIENT_ID)
    elif p == "github":
        return bool(settings.GITHUB_CLIENT_ID and settings.GITHUB_CLIENT_SECRET)
    return False


# --- Endpoints ---

@router.get("/providers", response_model=OAuthProvidersResponse)
def get_oauth_providers():
    """Return the configuration status of each social authentication provider."""
    return OAuthProvidersResponse(
        google=ProviderStatus(
            configured=is_provider_configured("google"),
            name="Google",
        ),
        apple=ProviderStatus(
            configured=is_provider_configured("apple"),
            name="Apple",
        ),
        github=ProviderStatus(
            configured=is_provider_configured("github"),
            name="GitHub",
        ),
    )


@router.get("/{provider}/authorize", response_model=OAuthAuthorizeResponse)
def authorize_oauth(provider: str, redirect_uri: Optional[str] = None):
    """
    Initiate OAuth authentication.
    Returns the official provider authorization URL if configured;
    otherwise returns an honest 503 error detailing missing credentials.
    """
    p = provider.lower()
    if p not in ("google", "apple", "github"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported OAuth provider '{provider}'. Supported providers: google, apple, github."
        )

    if not is_provider_configured(p):
        if p == "google":
            msg = "Google Sign-In is not configured on this server. GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET are missing in backend environment variables."
        elif p == "apple":
            msg = "Apple Sign-In is not configured on this server. APPLE_CLIENT_ID is missing in backend environment variables."
        else:
            msg = "GitHub Sign-In is not configured on this server. GITHUB_CLIENT_ID and GITHUB_CLIENT_SECRET are missing in backend environment variables."
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=msg
        )

    # Validate client-requested redirect_uri or fallback to settings
    effective_redirect_uri = None
    if redirect_uri and is_allowed_redirect_uri(redirect_uri):
        effective_redirect_uri = redirect_uri

    code_verifier = None
    code_challenge = None
    if p == "google":
        effective_redirect_uri = effective_redirect_uri or settings.GOOGLE_REDIRECT_URI
        code_verifier, code_challenge = generate_pkce_pair()
    elif p == "github":
        effective_redirect_uri = effective_redirect_uri or settings.GITHUB_REDIRECT_URI
    elif p == "apple":
        effective_redirect_uri = effective_redirect_uri or settings.APPLE_REDIRECT_URI

    state = generate_oauth_state(p, redirect_uri=effective_redirect_uri, code_verifier=code_verifier)

    if p == "google":
        params = {
            "client_id": settings.GOOGLE_CLIENT_ID,
            "redirect_uri": effective_redirect_uri,
            "response_type": "code",
            "scope": "openid email profile",
            "state": state,
            "access_type": "offline",
            "prompt": "select_account",
            "code_challenge": code_challenge,
            "code_challenge_method": "S256",
        }
        auth_url = f"https://accounts.google.com/o/oauth2/v2/auth?{urllib.parse.urlencode(params)}"
    elif p == "github":
        auth_url = (
            f"https://github.com/login/oauth/authorize"
            f"?client_id={settings.GITHUB_CLIENT_ID}"
            f"&redirect_uri={urllib.parse.quote(effective_redirect_uri, safe='')}"
            f"&scope=user:email%20read:user"
            f"&state={state}"
        )
    elif p == "apple":
        auth_url = (
            f"https://appleid.apple.com/auth/authorize"
            f"?client_id={settings.APPLE_CLIENT_ID}"
            f"&redirect_uri={urllib.parse.quote(effective_redirect_uri, safe='')}"
            f"&response_type=code%20id_token"
            f"&response_mode=form_post"
            f"&scope=name%20email"
            f"&state={state}"
        )
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unsupported provider.")

    return OAuthAuthorizeResponse(
        provider=p,
        authorization_url=auth_url,
        state=state,
    )


@router.post("/{provider}/callback", response_model=CustomerTokenResponse)
def oauth_callback(
    provider: str,
    payload: OAuthCallbackPayload,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Handle the OAuth authorization callback.
    Exchanges code for tokens, extracts identity securely, checks role/status,
    and returns a valid SmartServe session token.
    """
    p = provider.lower()
    if p not in ("google", "apple", "github"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported OAuth provider '{provider}'."
        )

    if not is_provider_configured(p):
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"{p.capitalize()} OAuth is not configured on this server."
        )

    # 1. State verification (Anti-CSRF & Anti-Replay)
    state_payload = verify_and_consume_oauth_state(payload.state, p, db)
    if not state_payload:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired OAuth state parameter. Please try logging in again."
        )

    # Effective redirect URI bound to state at authorize time
    bound_redirect_uri = state_payload.get("redirect_uri")
    code_verifier = state_payload.get("code_verifier")

    # 2. Token Exchange & Profile Extraction
    provider_user_id = None
    email = None
    full_name = None

    if p == "google":
        token_endpoint = "https://oauth2.googleapis.com/token"
        token_data = {
            "code": payload.code,
            "client_id": settings.GOOGLE_CLIENT_ID,
            "client_secret": settings.GOOGLE_CLIENT_SECRET,
            "redirect_uri": bound_redirect_uri or payload.redirect_uri or settings.GOOGLE_REDIRECT_URI,
            "grant_type": "authorization_code",
        }
        if code_verifier:
            token_data["code_verifier"] = code_verifier
        try:
            res = requests.post(token_endpoint, data=token_data, timeout=10)
            if not res.ok:
                logger.error(f"[Google OAuth] Token exchange failed: {res.text}")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Failed to authenticate with Google. Authorization code may be invalid or expired."
                )
            tokens = res.json()
            access_tok = tokens.get("access_token")

            # Fetch Google user profile
            prof_res = requests.get(
                "https://www.googleapis.com/oauth2/v3/userinfo",
                headers={"Authorization": f"Bearer {access_tok}"},
                timeout=10,
            )
            if not prof_res.ok:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to fetch Google user profile.")
            profile = prof_res.json()
            if profile.get("email_verified") is False:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Google account email is not verified. Please verify your email with Google or use standard sign in."
                )
            provider_user_id = str(profile.get("sub", ""))
            email = profile.get("email")
            full_name = profile.get("name")
        except requests.RequestException as e:
            logger.error(f"[Google OAuth] Network error: {e}")
            raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="Unable to reach Google OAuth services.")

    elif p == "github":
        token_endpoint = "https://github.com/login/oauth/access_token"
        token_data = {
            "code": payload.code,
            "client_id": settings.GITHUB_CLIENT_ID,
            "client_secret": settings.GITHUB_CLIENT_SECRET,
            "redirect_uri": bound_redirect_uri or payload.redirect_uri or settings.GITHUB_REDIRECT_URI,
        }
        try:
            res = requests.post(token_endpoint, json=token_data, headers={"Accept": "application/json"}, timeout=10)
            if not res.ok:
                logger.error(f"[GitHub OAuth] Token exchange failed: {res.text}")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Failed to authenticate with GitHub. Authorization code may be invalid or expired."
                )
            tokens = res.json()
            access_tok = tokens.get("access_token")
            if not access_tok:
                err_desc = tokens.get("error_description", "GitHub authentication error.")
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=err_desc)

            # Fetch user info
            gh_headers = {"Authorization": f"Bearer {access_tok}", "Accept": "application/json"}
            prof_res = requests.get("https://api.github.com/user", headers=gh_headers, timeout=10)
            if not prof_res.ok:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to fetch GitHub profile.")
            profile = prof_res.json()
            provider_user_id = str(profile.get("id", ""))
            full_name = profile.get("name") or profile.get("login")
            email = profile.get("email")

            # If email is private on GitHub profile, query emails endpoint
            if not email:
                emails_res = requests.get("https://api.github.com/user/emails", headers=gh_headers, timeout=10)
                if emails_res.ok:
                    emails_data = emails_res.json()
                    for em_item in emails_data:
                        if em_item.get("primary") and em_item.get("verified"):
                            email = em_item.get("email")
                            break
        except requests.RequestException as e:
            logger.error(f"[GitHub OAuth] Network error: {e}")
            raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="Unable to reach GitHub OAuth services.")

    elif p == "apple":
        token_endpoint = "https://appleid.apple.com/auth/token"
        token_data = {
            "code": payload.code,
            "client_id": settings.APPLE_CLIENT_ID,
            "client_secret": settings.APPLE_CLIENT_SECRET,
            "grant_type": "authorization_code",
            "redirect_uri": bound_redirect_uri or payload.redirect_uri or settings.APPLE_REDIRECT_URI,
        }
        try:
            res = requests.post(token_endpoint, data=token_data, timeout=10)
            if not res.ok:
                logger.error(f"[Apple OAuth] Token exchange failed: {res.text}")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Failed to authenticate with Apple. Authorization code may be invalid or expired."
                )
            tokens = res.json()
            id_token = tokens.get("id_token")
            if not id_token:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing Apple ID token.")
            # Decode claims from Apple ID token without signature verification for claims extraction (or with keys in prod)
            unverified_claims = jwt.get_unverified_claims(id_token)
            provider_user_id = unverified_claims.get("sub")
            email = unverified_claims.get("email")
            full_name = "Apple User"
        except Exception as e:
            logger.error(f"[Apple OAuth] Error: {e}")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to parse Apple authentication token.")

    if not provider_user_id or not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unable to retrieve verified email or identity from {p.capitalize()}."
        )

    clean_email = email.strip().lower()

    # 3. Secure Identity Mapping & Account Boundary Enforcement
    oauth_acc = (
        db.query(OAuthAccount)
        .filter(
            OAuthAccount.provider == p,
            OAuthAccount.provider_user_id == provider_user_id,
        )
        .first()
    )

    is_new_user = False
    requires_profile_completion = False

    if oauth_acc:
        # User already linked with this specific OAuth identity
        user = db.query(User).filter(User.id == oauth_acc.user_id).first()
        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="This account has been deactivated. Please contact SmartServe support."
            )
        if user.role != "customer":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Social authentication is only supported for customer accounts."
            )
        customer = db.query(Customer).filter(Customer.user_id == user.id).first()
        if not customer:
            customer = Customer(
                id=uuid.uuid4(),
                user_id=user.id,
                email=user.email,
                full_name=full_name or user.email.split("@")[0],
                phone=None,
                is_verified=True,
                is_active=True,
            )
            db.add(customer)
            db.commit()
            db.refresh(customer)

        # Check if customer profile has a valid phone number
        requires_profile_completion = not bool(customer.phone and customer.phone.strip())
    else:
        # Check if an existing User exists with this email address
        existing_user = db.query(User).filter(User.email == clean_email).first()
        if existing_user:
            # SECURITY REQUIREMENT: Do not automatically link existing account merely because email matches.
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=(
                    "An account with this email address already exists. "
                    "To prevent unauthorized account takeover, automatic account linking is disabled. "
                    "Please log in using your registered password."
                )
            )

        # Create new customer account with pending profile onboarding
        is_new_user = True
        requires_profile_completion = True
        random_pwd_hash = hash_password(secrets.token_urlsafe(32))
        user = User(
            id=uuid.uuid4(),
            email=clean_email,
            password_hash=random_pwd_hash,
            role="customer",
            is_active=True,
        )
        customer = Customer(
            id=uuid.uuid4(),
            user_id=user.id,
            email=clean_email,
            full_name=full_name or clean_email.split("@")[0],
            phone=None,
            password_hash=random_pwd_hash,
            is_verified=True,
            is_active=True,
        )
        oauth_acc = OAuthAccount(
            id=uuid.uuid4(),
            user_id=user.id,
            provider=p,
            provider_user_id=provider_user_id,
            email=clean_email,
        )
        db.add(user)
        db.add(customer)
        db.add(oauth_acc)
        db.commit()
        db.refresh(user)
        db.refresh(customer)

    # 4. Issue authenticated SmartServe JWT session
    token_jti = f"jwt_{uuid.uuid4().hex}"
    token = create_access_token({
        "sub": str(user.id),
        "role": "customer",
        "customer_id": str(customer.id),
        "email": user.email,
        "jti": token_jti,
        "pending_profile": requires_profile_completion,
    })

    # Track active session in database
    try:
        from app.services import security_service
        security_service.create_active_session(
            db, user_id=user.id, token_jti=token_jti,
            ip_address=request.client.host if request.client else "127.0.0.1",
            user_agent=request.headers.get("user-agent", "Web Browser")[:250],
            expires_in_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    except Exception:
        pass

    missing_fields = []
    if not customer.full_name or len(customer.full_name.strip()) < 2:
        missing_fields.append("full_name")
    if not (customer.phone and len(re.sub(r"\D", "", customer.phone)) >= 10):
        missing_fields.append("phone")

    loc = customer.preferences.get("location") if isinstance(customer.preferences, dict) else None

    return CustomerTokenResponse(
        access_token=token,
        customer_id=str(customer.id),
        user_id=str(user.id),
        email=customer.email,
        full_name=customer.full_name,
        phone=customer.phone,
        requires_profile_completion=requires_profile_completion,
        is_profile_complete=len(missing_fields) == 0,
        missing_profile_fields=missing_fields,
        is_new_user=is_new_user,
        location=loc,
    )
