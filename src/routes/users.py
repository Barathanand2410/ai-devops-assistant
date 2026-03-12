from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.db.database import get_db
from src.schemas import user_schema
from src.services import user_service
from src.utils.dependencies import verify_token

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/")
def get_users(
    db: Session = Depends(get_db),
    user: str = Depends(verify_token)
):
    return user_service.get_users(db)


@router.post("/")
def create_user(user: user_schema.UserCreate, db: Session = Depends(get_db)):
    return user_service.create_user(db, user)


@router.put("/{user_id}")
def update_user(user_id: int, user: user_schema.UserCreate, db: Session = Depends(get_db)):
    updated_user = user_service.update_user(db, user_id, user)

    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")

    return updated_user


@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    deleted_user = user_service.delete_user(db, user_id)

    if not deleted_user:
        raise HTTPException(status_code=404, detail="User not found")

    return {"message": "User deleted successfully"}

@router.get("/")
def get_users(
    db: Session = Depends(get_db),
    user: str = Depends(verify_token)
):
    return user_service.get_users(db)