from sqlalchemy.orm import Session
from src.db import models
from src.utils.auth import verify_password, create_access_token


def login_user(db: Session, email: str, password: str):

    user = db.query(models.User).filter(models.User.email == email).first()

    if not user:
        return None

    if not verify_password(password, user.password):
        return None

    token = create_access_token({"sub": user.email})

    return {
        "access_token": token,
        "token_type": "bearer"
    }