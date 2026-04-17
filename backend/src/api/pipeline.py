from fastapi import APIRouter
from src.services.ai_service import generate_pipeline

router = APIRouter()

@router.post("/generate-pipeline")
def create_pipeline(data: dict):

    language = data["language"]
    framework = data["framework"]
    ci_tool = data["ci_tool"]

    result = generate_pipeline(language, framework, ci_tool)

    return {"pipeline": result}