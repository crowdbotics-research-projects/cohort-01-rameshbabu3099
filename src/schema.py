from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class UserLogin(BaseModel):
    email: str
    password: str


class User(BaseModel):
    id: int
    username: str


class Token(BaseModel):
    username: str
    password: str


class Forgot(BaseModel):
    email: str
    password: str
    confirm_password: str


class Plans(BaseModel):
    id: int
    title: str
    description: str
    renewal_period: int
    tier: int
    discount: float

    class Config:
        orm_mode = True


class Magazines(BaseModel):
    id: int
    name: str
    description: str
    base_price: float
    plans: List[Plans]

    class Config:
        orm_mode = True


class SubscriptionBase(BaseModel):
    user_id: int
    magazine_id: int
    plan_id: int
    price: float
    renewal_date: str
    is_active: bool


class SubscriptionResponse(SubscriptionBase):
    id: int

    class Config:
        orm_mode = True


class SubscriptionCreate(BaseModel):
    magazine_id: int
    plan_id: int


class SubscriptionOut(BaseModel):
    id: int
    magazine_id: int
    plan_id: int
    price: float
    renewal_date: datetime
    is_active: bool

    class Config:
        orm_mode = True

class SubscriptionUpdate(BaseModel):
    magazine_id: int
    plan_id: int
    price: float
    renewal_date: datetime
    is_active: Optional[bool] = True  

    class Config:
        orm_mode = True