"""Authentication service handling logins, session cache, and permissions."""
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
