from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    username: str
    password: str
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    phone: Optional[str] = None

    class Config:
        orm_mode = True


class LoginRequest(BaseModel):
    username: str
    password: str


class ResetPasswordRequest(BaseModel):
    email: str
    new_password: str


# Pydantic model for creating a magazine
class MagazineCreate(BaseModel):
    name: str
    description: str
    base_price: float
    discount: Optional[float] = Field(default=10.0)
    discount_half_yearly: Optional[float] = Field(default=10.0)
    discount_quarterly: Optional[float] = None
    discount_annual: Optional[float] = None

    class Config:
        orm_mode = True


class PlanResponse(BaseModel):
    id: int
    title: str
    description: str
    renewal_period: int


class PlanModel(BaseModel):
    title: str
    description: str
    renewal_period: int


class SubscriptionCreate(BaseModel):
    user_id: int
    magazine_id: int
    plan_id: int
    price: float
    # price_at_renewal: int
    next_renewal_date: datetime

    class Config:
        orm_mode = True


class SubscriptionUpdate(BaseModel):
    magazine_id: int = None  # Optional field
    plan_id: int = None  # Optional field
    price: float = None  # Optional field
    next_renewal_date: datetime = None  # Optional field

    class Config:
        orm_mode = True


class SubscriptionResponse(BaseModel):
    id: int
    user_id: int
    magazine_id: int
    plan_id: int
    price: float
    price_at_renewal: float
    next_renewal_date: datetime
    is_active: bool
