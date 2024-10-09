from .db import get_db
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from . import schema
from .auth import *
from .models import *
from typing import List
from .utils import *
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from fastapi import Depends, HTTPException, Security


router = APIRouter()


@router.post("/users/register", response_model=None)
def register_user(user: RegisterRequest, db: Session = Depends(get_db)):
    db_user = Users(
        username=user.username,
        email=user.email,
        password=user.password,
        address=user.address,
        phone=user.phone,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.post("/users/login")
def login(user: LoginRequest, db: Session = Depends(get_db)):
    db_user = db.query(Users).filter(Users.username == user.username).first()
    if db_user and db_user.password == user.password:  # Consider using hashed passwords
        access_token = create_access_token({"sub": user.username})
        refresh_token = create_refresh_token({"sub": user.username})
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "status_code": 200,
            "text": "Success",
        }
    raise HTTPException(status_code=400, detail="Invalid credentials")


@router.post("/users/reset-password")
def reset_password(email: str, db: Session = Depends(get_db)):
    user = db.query(Users).filter(Users.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    reset_token = create_refresh_token(
        {"sub": user.username}
    )  # Replace with actual token generation logic
    print(f"Generated reset token for {user.email}: {reset_token}")
    return {"message": "Password reset email sent"}


@router.post("/users/token/refresh")
def user_token_refresh(
    token: str = Security(oauth2_scheme), db: Session = Depends(get_db)
):
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(Users).filter(Users.username == payload.get("sub")).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    refresh_token = create_refresh_token(
        {"sub": user.username}
    )  # Replace with actual token generation logic
    access_token = create_access_token({"sub": user.username})
    return {"refresh_token": refresh_token, "access_token": access_token}


@router.get("/users/me")
def verify_user_token(
    token: str = Security(oauth2_scheme), db: Session = Depends(get_db)
):
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(Users).filter(Users.username == payload.get("sub")).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"username": user.username, "status": 200}


@router.delete("/users/deactivate/{username}")
def deactivate_user(username: str, db: Session = Depends(get_db)):
    db_user = db.query(Users).filter(Users.username == username).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    db_user.is_active = (
        False  # Assuming there is an `is_active` field in the User model
    )
    db.commit()
    db.refresh(db_user)
    return db_user


@router.get("/magazines/", response_model=List[MagazineCreate])
def get_magazines(db: Session = Depends(get_db)):
    try:
        magazines = db.query(Magazines).all()
        return magazines
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/magazines/", response_model=None)
def create_magazine(magazine: MagazineCreate, db: Session = Depends(get_db)):
    db_magazine = Magazines(**magazine.dict())
    db.add(db_magazine)
    db.commit()
    db.refresh(db_magazine)
    return db_magazine


@router.put("/magazines/{magazine_id}", response_model=MagazineCreate)
def update_magazine(
    magazine_id: int, magazine: MagazineCreate, db: Session = Depends(get_db)
):
    db_magazine = db.query(Magazines).filter(Magazines.id == magazine_id).first()
    if db_magazine is None:
        raise HTTPException(status_code=404, detail="Magazine not found")

    for key, value in magazine.dict().items():
        setattr(db_magazine, key, value)

    db.commit()
    db.refresh(db_magazine)
    return db_magazine


@router.delete("/magazines/{magazine_id}", response_model=MagazineCreate)
def delete_magazine(magazine_id: int, db: Session = Depends(get_db)):
    db_magazine = db.query(Magazines).filter(Magazines.id == magazine_id).first()
    if db_magazine is None:
        raise HTTPException(status_code=404, detail="Magazine not found")

    db.delete(db_magazine)
    db.commit()
    return db_magazine


@router.get("/magazines/{magazine_id}", response_model=MagazineCreate)
def get_magazine_by_id(magazine_id: int, db: Session = Depends(get_db)):
    db_magazine = db.query(Magazines).filter(Magazines.id == magazine_id).first()
    if db_magazine is None:
        raise HTTPException(status_code=404, detail="Magazine not found")
    return db_magazine


@router.post("/plans/", response_model=PlanResponse)
def create_plan(plan: PlanModel, db: Session = Depends(get_db)):
    if plan.renewal_period == 0:
        raise HTTPException(status_code=422, detail="Renewal period cannot be zero")
    db_plan = Plans(**plan.dict())
    db.add(db_plan)
    db.commit()
    db.refresh(db_plan)
    return db_plan


@router.get("/plans/", response_model=List[PlanResponse])
def get_all_plans(db: Session = Depends(get_db)):
    plans = db.query(Plans).all()
    return plans


@router.delete("/plans/", response_model=str)
def delete_all_plans(db: Session = Depends(get_db)):
    """
    Delete all subscription plans.
    """
    try:
        # Delete all plans from the database
        db.query(Plans).delete()
        db.commit()  # Commit the changes
        return "All plans deleted successfully."
    except Exception as e:
        db.rollback()  # Rollback in case of error
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/plans/{plan_id}", response_model=PlanResponse)
def update_plan(plan_id: int, plan: PlanModel, db: Session = Depends(get_db)):
    db_plan = db.query(Plans).filter(Plans.id == plan_id).first()
    if db_plan is None:
        raise HTTPException(status_code=404, detail="Plan not found")

    for key, value in plan.dict().items():
        setattr(db_plan, key, value)

    db.commit()
    db.refresh(db_plan)
    return db_plan


@router.delete("/plans/{plan_id}", response_model=PlanResponse)
def delete_plan(plan_id: int, db: Session = Depends(get_db)):
    db_plan = db.query(Plans).filter(Plans.id == plan_id).first()
    if db_plan is None:
        raise HTTPException(status_code=404, detail="Plan not found")

    db.delete(db_plan)
    db.commit()
    return db_plan


@router.get("/plans/{plan_id}", response_model=PlanResponse)
def get_magazine_by_id(plan_id: int, db: Session = Depends(get_db)):
    db_plan = db.query(Plans).filter(Plans.id == plan_id).first()
    if db_plan is None:
        raise HTTPException(status_code=404, detail="Magazine not found")
    return db_plan


@router.post("/subscriptions/", response_model=SubscriptionResponse)
def create_subscription(
    subscription: SubscriptionCreate, db: Session = Depends(get_db)
):
    db_subscription = Subscriptions(**subscription.dict())
    db.add(db_subscription)
    db.commit()
    db.refresh(db_subscription)
    return db_subscription


@router.get("/subscriptions/", response_model=List[SubscriptionResponse])
def get_all_subscriptions(db: Session = Depends(get_db)):
    subs = db.query(Subscriptions).all()
    return subs


@router.put("/subscriptions/{subscription_id}", response_model=SubscriptionResponse)
def update_subscription(
    subscription_id: int,
    subscription: SubscriptionCreate,
    db: Session = Depends(get_db),
):
    db_subscription = (
        db.query(Subscriptions).filter(Subscriptions.id == subscription_id).first()
    )
    if db_subscription is None:
        raise HTTPException(status_code=404, detail="Subscription not found")

    for key, value in subscription.dict().items():
        setattr(db_subscription, key, value)

    db.commit()
    db.refresh(db_subscription)
    return db_subscription


@router.delete("/subscriptions/{subscription_id}", response_model=SubscriptionResponse)
def delete_subscription(subscription_id: int, db: Session = Depends(get_db)):
    db_subscription = (
        db.query(Subscriptions).filter(Subscriptions.id == subscription_id).first()
    )
    if db_subscription is None:
        raise HTTPException(status_code=404, detail="Subscription not found")

    db_subscription.is_active = False
    # db.delete(db_subscription)
    db.commit()
    db.refresh(db_subscription)
    return db_subscription


@router.get("/subscriptions/{subscription_id}", response_model=SubscriptionResponse)
def get_subscription_by_id(subscription_id: int, db: Session = Depends(get_db)):
    db_subscription = (
        db.query(Subscriptions).filter(Subscriptions.id == subscription_id).first()
    )
    if db_subscription is None:
        raise HTTPException(status_code=404, detail="Subscription not found")
    return db_subscription
