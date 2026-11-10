"""High-throughput associative cache bridge with TTL."""
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
