"""Parietal semantic data contracts, schemas, and DTOs."""
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
