from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.responses import FileResponse

from src.db.database import get_db
from src.services.ai_service import (
    generate_pipeline,
    explain_pipeline_service,
    fix_error_service
)
from src.services.query_service import save_query
from src.models.ai_query import AIQuery
from src.schemas.devops_query import DevOpsQuery

router = APIRouter(prefix="/ai", tags=["AI DevOps"])


# ===============================
# 🚀 GENERATE PIPELINE
# ===============================
@router.post("/devops-query")
def devops_query(request: DevOpsQuery, db: Session = Depends(get_db)):

    result = generate_pipeline(request.query, request.tool)

    saved = save_query(db, request.query, result)

    return {
        "status": "success",
        "id": saved.id,
        "query": request.query,
        "tool": request.tool,
        "generated_script": result
    }


# ===============================
# 📜 GET HISTORY (LATEST FIRST)
# ===============================
@router.get("/history")
def get_history(db: Session = Depends(get_db)):
    return db.query(AIQuery).order_by(AIQuery.id.desc()).all()


# ===============================
# 📥 DOWNLOAD SCRIPT
# ===============================
@router.get("/download/{query_id}")
def download_script(query_id: int, db: Session = Depends(get_db)):

    query = db.query(AIQuery).filter(AIQuery.id == query_id).first()

    if not query:
        return {"error": "Query not found"}

    file_path = f"script_{query_id}.txt"

    with open(file_path, "w") as f:
        f.write(query.response)

    return FileResponse(
        path=file_path,
        filename=f"devops_script_{query_id}.txt",
        media_type="text/plain"
    )


# ===============================
# 🗑️ DELETE QUERY
# ===============================
@router.delete("/query/{query_id}")
def delete_query(query_id: int, db: Session = Depends(get_db)):

    query = db.query(AIQuery).filter(AIQuery.id == query_id).first()

    if not query:
        return {"message": "Query not found"}

    db.delete(query)
    db.commit()

    return {"message": "Deleted successfully"}


# ===============================
# 🧠 EXPLAIN PIPELINE
# ===============================
@router.post("/explain")
def explain_pipeline(data: dict):

    script = data.get("script")

    if not script:
        return {"error": "Script is required"}

    explanation = explain_pipeline_service(script)

    return {"explanation": explanation}


# ===============================
# 🛠️ FIX ERROR
# ===============================
@router.post("/fix-error")
def fix_error(data: dict):

    error = data.get("error")

    if not error:
        return {"error": "Error input is required"}

    solution = fix_error_service(error)

    return {"solution": solution}