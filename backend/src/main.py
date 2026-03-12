from fastapi import FastAPI
from src.routes.ai_routes import router as ai_router
from src.db.database import Base, engine
from src.db import models
from src.models.ai_query import AIQuery
from src.routes.status import router as status_router
from src.routes.users import router as users_router
from src.routes.health import router as health_router
from src.routes.auth import router as auth_router

from src.config.settings import settings

# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI()

app.include_router(ai_router)

@app.get("/")
def root():
    return {"message": "AI DevOps Assistant Running"}

# Include routers
app.include_router(status_router)
app.include_router(users_router)
app.include_router(health_router)
app.include_router(auth_router)