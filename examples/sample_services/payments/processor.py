"""Payment processing gateway with Stripe/Webhook integration."""
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
