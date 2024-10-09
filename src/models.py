from sqlalchemy import Column, Integer, String

from .db import Base
from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    ForeignKey,
    Date,
    Boolean,
)


class Users(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    address = Column(String(200), nullable=True)
    phone = Column(String(15), nullable=True)


class Magazines(Base):
    __tablename__ = "magazine"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(String(200), nullable=False)
    base_price = Column(Integer, nullable=False)
    discount = Column(Float, nullable=False, default=10.0)
    discount_half_yearly = Column(Float, nullable=False, default=10.0)
    discount_quarterly = Column(Float, nullable=True)
    discount_annual = Column(Float, nullable=True)


class Plans(Base):
    __tablename__ = "plan"

    id = Column(Integer, primary_key=True)
    title = Column(String(100), unique=True, nullable=False)
    description = Column(String(200), nullable=False)
    renewal_period = Column(Integer, nullable=False)

    def __init__(self, title, description, renewal_period):
        self.title = title
        self.description = description
        self.renewal_period = renewal_period


class Subscriptions(Base):
    __tablename__ = "subscription"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    magazine_id = Column(Integer, ForeignKey("magazine.id"), nullable=False)
    plan_id = Column(Integer, ForeignKey("plan.id"), nullable=False)
    price = Column(Integer, nullable=False)
    price_at_renewal = Column(Integer, nullable=False, default=0)
    next_renewal_date = Column(Date, nullable=False, default="2021-01-01")
    is_active = Column(Boolean, nullable=False, default=True)

    user = relationship("Users", backref="subscriptions")
    magazine = relationship("Magazines", backref="subscriptions")
    plan = relationship("Plans", backref="subscriptions")
