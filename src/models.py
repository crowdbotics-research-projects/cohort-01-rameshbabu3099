from sqlalchemy import Column, Integer, String
from .db import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date,DateTime, Boolean


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)



class Magazine(Base):
    __tablename__ = "magazines"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    base_price = Column(Float)

    plans = relationship("Plan", back_populates="magazine")


class Plan(Base):
    __tablename__ = "plans"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    renewal_period = Column(Integer)
    tier = Column(Integer)
    discount = Column(Float)
    magazine_id = Column(Integer, ForeignKey("magazines.id"))

    magazine = relationship("Magazine", back_populates="plans")


class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    magazine_id = Column(Integer, ForeignKey('magazines.id'))
    plan_id = Column(Integer, ForeignKey('plans.id'))
    price = Column(Float)
    renewal_date = Column(Date)
    is_active = Column(Boolean, default=True)

    magazine = relationship("Magazine")
    plan = relationship("Plan")
