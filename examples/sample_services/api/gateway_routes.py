"""Occipital external sensory interface and API endpoints."""
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
