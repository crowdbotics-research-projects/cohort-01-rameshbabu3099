from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from .schema import *
from .models import *
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from .db import get_db
from fastapi import APIRouter, Depends
from .schema import *


def create_subscription(db: Session, user_id: int, subscription: SubscriptionCreate):
    # Check if the user already has an active subscription for this magazine and plan
    existing_subscription = (
        db.query(Subscription)
        .filter(
            Subscription.user_id == user_id,
            Subscription.magazine_id == subscription.magazine_id,
            Subscription.plan_id == subscription.plan_id,
            Subscription.is_active == True,
        )
        .first()
    )

    if existing_subscription:
        raise ValueError(
            "Active subscription already exists for this magazine and plan."
        )

    magazine = (
        db.query(Magazine).filter(Magazine.id == subscription.magazine_id).first()
    )
    plan = db.query(Plan).filter(Plan.id == subscription.plan_id).first()

    if not magazine or not plan:
        raise ValueError("Magazine or plan not found.")

    # Calculate the price at renewal
    price = magazine.base_price * (1 - plan.discount)
    if price <= 0:
        raise ValueError("Price must be greater than zero.")

    # Calculate the renewal date
    renewal_date = datetime.utcnow() + timedelta(days=plan.renewal_period * 30)

    # Deactivate any existing subscription for this magazine and user
    db.query(Subscription).filter(
        Subscription.user_id == user_id,
        Subscription.magazine_id == subscription.magazine_id,
    ).update({"is_active": False}, synchronize_session=False)

    new_subscription = Subscription(
        user_id=user_id,
        magazine_id=subscription.magazine_id,
        plan_id=subscription.plan_id,
        price=price,
        renewal_date=renewal_date,
        is_active=True,
    )
    db.add(new_subscription)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise ValueError("Error creating subscription.")
    db.refresh(new_subscription)

    return new_subscription


def get_user_subscriptions(db: Session, user_id: int):
    return (
        db.query(Subscription)
        .filter(Subscription.user_id == user_id, Subscription.is_active == True)
        .all()
    )


def deactivate_subscription(db: Session, subscription_id: int):
    db_subscription = (
        db.query(Subscription).filter(Subscription.id == subscription_id).first()
    )
    if db_subscription:
        db_subscription.is_active = False
        db.commit()
        db.refresh(db_subscription)
    return db_subscription


def update_subscription(
    db: Session, subscription_id: int, subscription_update: SubscriptionUpdate
):
    # Find the existing active subscription
    db_subscription = (
        db.query(Subscription).filter(Subscription.id == subscription_id).first()
    )

    if db_subscription:
        # Deactivate the existing subscription
        db_subscription.is_active = False
        db.commit()

        # Create a new subscription with updated details
        new_subscription = Subscription(
            user_id=db_subscription.user_id,
            magazine_id=subscription_update.magazine_id,
            plan_id=subscription_update.plan_id,
            price=calculate_price(
                subscription_update.magazine_id, subscription_update.plan_id, db
            ),
            renewal_date=calculate_renewal_date(subscription_update.plan_id, db),
            is_active=True,
        )

        db.add(new_subscription)
        db.commit()
        db.refresh(new_subscription)
        return new_subscription

    # Handle the case where the subscription is not found
    raise HTTPException(status_code=404, detail="Subscription not found")


def calculate_price(magazine_id: int, plan_id: int, db) -> float:
    # Assuming you have a way to get base price and discount percentage
    # Implement your pricing logic here
    magazine = db.query(Magazine).filter(Magazine.id == magazine_id).first()
    if magazine:
        base_price = magazine.base_price
    plan = db.query(Plan).filter(Plan.id == plan_id).first()
    if plan:
        discount = plan.discount

    return base_price * (1 - discount)


def calculate_renewal_date(plan_id: int, db) -> datetime:
    # Calculate renewal date based on the plan's renewal period
    plan = db.query(Plan).filter(Plan.id == plan_id).first()
    if plan:
        renewal_period = plan.renewal_period
        print(renewal_period,"ggg'")
    return add_months(datetime.now(), renewal_period)



def add_months(source_date: datetime, months: int) -> datetime:
    month = source_date.month - 1 + months
    year = source_date.year + month // 12
    month = month % 12 + 1
    day = min(source_date.day, [31,
        29 if year % 4 == 0 and not year % 100 == 0 or year % 400 == 0 else 28,
        31, 30, 31, 30, 31, 31, 30, 31, 30, 31][month-1])
    return datetime(year, month, day)