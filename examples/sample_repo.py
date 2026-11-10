"""
Realistic multi-service codebase generator to demonstrate SynapseGraph.
Creates real Python files with cross-module dependencies, API routes, database pools, and models.
"""

import os

SERVICES = {
    "auth/jwt_handler.py": '''"""JWT security and cryptographical token handler."""
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
''',

    "auth/auth_service.py": '''"""Authentication service handling logins, session cache, and permissions."""
from auth.jwt_handler import JWTManager
from cache.redis_bridge import RedisMemoryBridge
from db.connection_pool import DatabasePool
from models.user import TokenPayload, UserDTO

class AuthService:
    """Core executive authentication service."""
    def __init__(self, jwt_mgr: JWTManager, cache: RedisMemoryBridge, db: DatabasePool):
        self.jwt = jwt_mgr
        self.cache = cache
        self.db = db

    def login(self, username: str, password_hash: str) -> str:
        """Authenticates user credentials, queries DB, and returns token."""
        user = self.db.find_user_by_credentials(username, password_hash)
        if not user:
            raise PermissionError("Invalid user credentials")
        payload = TokenPayload(user_id=user.user_id, role=user.role)
        token = self.jwt.sign_token(payload)
        self.cache.store_session(user.user_id, token)
        return token

    def authenticate_request(self, token: str) -> UserDTO:
        """Validates incoming HTTP Bearer token against cache and crypto validator."""
        payload = self.jwt.verify_token(token)
        if not payload:
            raise PermissionError("Token signature invalid or expired")
        cached = self.cache.get_session(payload.user_id)
        if not cached:
            raise PermissionError("Session revoked in cache")
        return self.db.get_user_by_id(payload.user_id)
''',

    "cache/redis_bridge.py": '''"""High-throughput associative cache bridge with TTL."""
from typing import Optional, Dict

class RedisMemoryBridge:
    """Associative bridge for fast session recall and edge caching."""
    def __init__(self, host: str = "localhost", port: int = 6379):
        self.host = host
        self.port = port
        self._store: Dict[str, str] = {}

    def store_session(self, user_id: str, session_token: str, ttl_seconds: int = 3600):
        """Indexes active session token with expiration."""
        self._store[f"session:{user_id}"] = session_token

    def get_session(self, user_id: str) -> Optional[str]:
        """Fetches active session token from cache."""
        return self._store.get(f"session:{user_id}")

    def invalidate_user(self, user_id: str):
        """Purges active cache entry upon logout or security breach."""
        self._store.pop(f"session:{user_id}", None)
''',

    "db/connection_pool.py": '''"""Database connection pooling and transactional query executor."""
from typing import Optional, List, Dict
from models.user import UserDTO

class DatabasePool:
    """Manages database connection lifecycle and transaction safety."""
    def __init__(self, dsn: str = "postgresql://cluster:5432/main"):
        self.dsn = dsn
        self.active_conns = 10

    def find_user_by_credentials(self, username: str, pass_hash: str) -> Optional[UserDTO]:
        """Executes indexed credential lookup on primary replica."""
        return UserDTO(user_id="usr_88291", username=username, role="admin", email=f"{username}@mesh.net")

    def get_user_by_id(self, user_id: str) -> UserDTO:
        """Retrieves hydrated user record from primary database."""
        return UserDTO(user_id=user_id, username="dev_lead", role="admin", email="dev@mesh.net")

    def update_billing_status(self, user_id: str, tier: str):
        """Persists customer subscription tier."""
        pass
''',

    "models/user.py": '''"""Parietal semantic data contracts, schemas, and DTOs."""
from dataclasses import dataclass
from typing import Optional

@dataclass
class TokenPayload:
    """Semantic JWT claims contract."""
    user_id: str
    role: str

@dataclass
class UserDTO:
    """Customer entity representation."""
    user_id: str
    username: str
    role: str
    email: str
    tier: str = "enterprise"

@dataclass
class PaymentRequest:
    """Payment intent specification."""
    user_id: str
    amount_cents: int
    currency: str = "USD"
''',

    "payments/processor.py": '''"""Payment processing gateway with Stripe/Webhook integration."""
from models.user import PaymentRequest
from db.connection_pool import DatabasePool
from cache.redis_bridge import RedisMemoryBridge

class PaymentProcessor:
    """Executes idempotent payment intents and updates customer entitlements."""
    def __init__(self, db: DatabasePool, cache: RedisMemoryBridge):
        self.db = db
        self.cache = cache

    def process_charge(self, req: PaymentRequest) -> str:
        """Dispatches charge transaction to card network and updates customer tier."""
        if req.amount_cents <= 0:
            raise ValueError("Invalid charge amount")
        charge_id = f"ch_{req.user_id}_992"
        self.db.update_billing_status(req.user_id, "premium_active")
        self.cache.invalidate_user(req.user_id) # Force token payload refresh
        return charge_id
''',

    "api/gateway_routes.py": '''"""Occipital external sensory interface and API endpoints."""
from auth.auth_service import AuthService
from payments.processor import PaymentProcessor
from models.user import PaymentRequest

# MCP / Web sensory endpoints
def route_login(auth: AuthService, credentials: dict):
    """POST /auth/login - External authentication sensory ingress."""
    return auth.login(credentials.get("username"), credentials.get("password"))

def route_checkout(payment: PaymentProcessor, auth: AuthService, token: str, amount: int):
    """POST /payments/checkout - Secure charge endpoint with bearer auth validation."""
    user = auth.authenticate_request(token)
    req = PaymentRequest(user_id=user.user_id, amount_cents=amount)
    return payment.process_charge(req)

def route_profile(auth: AuthService, token: str):
    """GET /user/profile - Returns verified profile payload."""
    return auth.authenticate_request(token)
'''
}

def create_sample_files(base_dir: str):
    """Writes the sample codebase to disk."""
    for rel_path, code in SERVICES.items():
        full_p = os.path.join(base_dir, rel_path)
        os.makedirs(os.path.dirname(full_p), exist_ok=True)
        with open(full_p, "w", encoding="utf-8") as f:
            f.write(code)
    print(f"Created {len(SERVICES)} sample microservice files in {base_dir}")
