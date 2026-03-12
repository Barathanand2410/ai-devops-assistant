from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from src.db import models
from src.schemas import user_schema
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    return pwd_context.hash(password[:72])


def create_user(db: Session, user: user_schema.UserCreate):
    hashed_password = hash_password(user.password)

    new_user = models.User(
        name=user.name,
        email=user.email,
        password=hashed_password
    )

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

    except IntegrityError:
        db.rollback()
        return {"error": "Email already exists"}


def get_users(db: Session):
    return db.query(models.User).all()