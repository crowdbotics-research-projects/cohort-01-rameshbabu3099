from .db import get_db
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from . import schema
from .auth import *
from .models import *
from typing import List
from .utils import *

from fastapi import FastAPI, Header


router = APIRouter()

from fastapi.security import HTTPBearer

app = FastAPI()
security = HTTPBearer()


@app.get("/")
def main(authorization: str = Depends(security)):
    return authorization.credentials


@router.post("/register_user/")
def register(user: schema.UserCreate, db: Session = Depends(get_db)):
    return register(db=db, user=user)


@router.post("/login")
def user_login(user: schema.UserLogin, db: Session = Depends(get_db)):
    print(user, "uuuu")
    return login(db=db, email=user.email, password=user.password)


@router.post("/forgot-password/")
def forgot_password(user: schema.Forgot, db: Session = Depends(get_db)):
    return forgot_password(
        db=db,
        email=user.email,
        password=user.password,
        confirm_password=user.confirm_password,
    )


def get_magazines_with_plans(db: Session):
    return db.query(Magazine).all()


@router.get("/magazines/", response_model=List[schema.Magazines])
def read_magazines(db: Session = Depends(get_db)):

    magazines = get_magazines_with_plans(db)
    return magazines


@router.post("/subscriptions/", response_model=schema.SubscriptionOut)
def create_user_subscription(
    subscription: schema.SubscriptionCreate,
    db: Session = Depends(get_db),
    current_user: schema.User = Depends(get_current_user),
):
    print(current_user, "'ccccc")
    user_id = current_user.id
    db_subscription = create_subscription(db, user_id, subscription)
    return db_subscription


@router.get("/subscriptions/", response_model=List[schema.SubscriptionOut])
def read_user_subscriptions(
    db: Session = Depends(get_db), user: schema.User = Depends(get_current_user)
):
    user_id = user.id
    return get_user_subscriptions(db, user_id)


@router.delete(
    "/subscriptions/{subscription_id}", response_model=schema.SubscriptionOut
)
def cancel_subscription(subscription_id: int, db: Session = Depends(get_db)):
    db_subscription = deactivate_subscription(db, subscription_id)
    if db_subscription is None:
        raise HTTPException(status_code=404, detail="Subscription not found")
    return db_subscription


@router.put("/subscriptions/{subscription_id}")
def update_user_subscription(
    subscription_id: int,
    subscription_update: SubscriptionUpdate,
    db: Session = Depends(get_db),
):
    db_subscription = update_subscription(db, subscription_id, subscription_update)
    if db_subscription is None:
        raise HTTPException(status_code=404, detail="Subscription not found")
    return db_subscription
