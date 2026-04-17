from fastapi import APIRouter

router = APIRouter()

@router.get("/status")
def status():
    return {"message": "Backend is running"}