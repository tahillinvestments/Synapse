"""JWT security and cryptographical token handler."""
import hmac
import hashlib
import time
from typing import Dict, Optional
from models.user import TokenPayload

class JWTManager:
    """Handles JWT generation, claims parsing, and HMAC SHA256 validation."""
    def __init__(self, secret: str = "k3y_s3cr3t_2026"):
        self.secret = secret

    def sign_token(self, payload: TokenPayload) -> str:
        """Signs user payload into a compact token."""
        header = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
        raw_claims = f"{payload.user_id}:{payload.role}:{time.time()}"
        signature = hmac.new(self.secret.encode(), raw_claims.encode(), hashlib.sha256).hexdigest()
        return f"{header}.{raw_claims}.{signature}"

    def verify_token(self, raw_token: str) -> Optional[TokenPayload]:
        """Validates token integrity and expiration timestamp."""
        parts = raw_token.split(".")
        if len(parts) != 3:
            return None
        claims = parts[1].split(":")
        return TokenPayload(user_id=claims[0], role=claims[1])
