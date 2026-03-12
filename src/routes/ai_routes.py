from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.responses import FileResponse   

from src.db.database import get_db
from src.services.ai_service import generate_devops_script
from src.services.query_service import save_query
from src.models.ai_query import AIQuery
import os
router = APIRouter(prefix="/ai", tags=["AI DevOps"])


@router.post("/devops-query")
def devops_query(query: str, db: Session = Depends(get_db)):

    result = generate_devops_script(query)

    save_query(db, query, result)

    return {
        "status": "success",
        "query": query,
        "generated_script": result
    }


@router.get("/history")
def get_history(db: Session = Depends(get_db)):

    queries = db.query(AIQuery).all()

    return queries

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

@router.get("/search")
def search_queries(keyword: str, db: Session = Depends(get_db)):

    results = db.query(AIQuery).filter(
        AIQuery.query.contains(keyword)
    ).all()

    return results

@router.delete("/query/{query_id}")
def delete_query(query_id: int, db: Session = Depends(get_db)):

    query = db.query(AIQuery).filter(AIQuery.id == query_id).first()

    if not query:
        return {"message": "Query not found"}

    db.delete(query)
    db.commit()

    return {"message": "Query deleted successfully"}