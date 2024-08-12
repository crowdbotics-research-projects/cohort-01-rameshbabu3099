from sqlalchemy.orm import Session
from . import schema
from .models import *
from fastapi import HTTPException
from jose import JWTError, jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import FastAPI, Depends, HTTPException, status
from .db import get_db
from fastapi.security import OAuth2PasswordBearer, HTTPBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

SECRET_KEY = "GRHTYJKLUJSIEMDJSERUJAWEWRAW"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 200

# For simple Bearer tokens
bearer_scheme = HTTPBearer()


def get_user(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def register(db: Session, user: schema.UserCreate):
    hashed_password = get_password_hash(user.password)
    if get_user(db, user.username):
        raise HTTPException(status_code=400, detail="Username already registered")

    db_user = User(username=user.username, email=user.email, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"msg": "User registered successfully"}


def login(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    if not verify_password(password, user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


def forgot_password(db: Session, email: str, password: str, confirm_password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Email not found")
    if password == confirm_password:
        user.password = get_password_hash(password)
        db.commit()
        db.refresh(user)

    # Implement email sending logic here for resetting the password
    return {"message": "Password rest successfully"}


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    # def get_current_user(
    #     token: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJSYW1lc2giLCJleHAiOjE3MjM0OTQxMTl9.I5UvK5lDDCR-d6bcYBUosnYUvhbGqLvECjeBwVd7veE",
    #     db: Session = Depends(get_db),
    # ):
    print(token, "jjjjjjjjjjjj")
    payload = decode_access_token(token)
    print(payload, "payload")
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = db.query(User).filter(User.username == payload.get("sub")).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    print(user, "uuuuuuuuuuuuuu")
    print(user.id)  # Output: 1
    print(user.username)
    return user
