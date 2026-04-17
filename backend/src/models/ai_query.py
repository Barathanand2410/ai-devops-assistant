from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from src.db.database import Base


class AIQuery(Base):
    __tablename__ = "ai_queries"

    id = Column(Integer, primary_key=True, index=True)
    query = Column(String, nullable=False)
    response = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)