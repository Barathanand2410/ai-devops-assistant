from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routes import ai_routes

# Routers
from src.routes.ai_routes import router as ai_router
from src.routes.status import router as status_router
from src.routes.users import router as users_router
from src.routes.health import router as health_router
from src.routes.auth import router as auth_router
from src.api.pipeline import router as pipeline_router

# DB
from src.db.database import Base, engine

# ✅ Create DB tables
Base.metadata.create_all(bind=engine)

# ✅ Create ONE FastAPI app only
app = FastAPI(title="AI DevOps Assistant")

# ✅ CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Register all routes
app.include_router(ai_router)
app.include_router(status_router)
app.include_router(users_router)
app.include_router(health_router)
app.include_router(auth_router)
app.include_router(pipeline_router)

# ✅ Root check
@app.get("/")
def root():
    return {"message": "AI DevOps Assistant Running"}