from sqlalchemy.orm import Session
from src.models.ai_query import AIQuery


def save_query(db: Session, query: str, response: str):

    record = AIQuery(
        query=query,
        response=response
    )

    db.add(record)
    db.commit()
    db.refresh(record)

    return record