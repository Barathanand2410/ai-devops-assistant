from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.db.database import get_db
from src.schemas.auth_schema import LoginRequest
from src.services import auth_service

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):

    user = auth_service.login_user(db, data.email, data.password)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    return user