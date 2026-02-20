"""
DeepRow Analytics Engine - FastAPI Backend

Self-service data analytics for non-technical users:
- Automatic data profiling (detects types, issues, quality)
- Semantic layer (auto-generates business metrics/dimensions)
- Trust-first design (every number is explainable)
- Domain-agnostic (works for teachers, nurses, researchers, business owners)

Routes:
POST   /api/auth/signup          - Create account
POST   /api/auth/login           - Get JWT token
GET    /api/auth/me              - Current user
POST   /api/projects             - Create project
GET    /api/projects             - List projects
GET    /api/projects/{id}        - Get project
DELETE /api/projects/{id}        - Delete project
POST   /api/datasets/upload/{id} - Upload CSV/Excel
GET    /api/datasets/{id}        - Get dataset with profiling
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import SQLAlchemyError
import logging

from app.core.database import init_db
from app.api import auth, projects, datasets

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI
app = FastAPI(
    title="DeepRow Analytics Engine",
    description="Self-service data analytics that auto-detects data types and generates insights",
    version="1.0.0"
)

# Enable CORS for frontend (localhost and production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",      # Vite dev
        "http://localhost:3000",      # Alternative dev
        "http://localhost:8080",      # Vue dev
        "https://deeprow.vercel.app", # Production
        "*"                           # TODO: Remove in production
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database on startup
@app.on_event("startup")
async def startup():
    """Initialize database and create tables"""
    try:
        init_db()
        logger.info("✅ Database initialized successfully")
    except Exception as e:
        logger.warning(f"⚠️ Database initialization failed (continuing without DB): {e}")
        logger.warning("The API will work with in-memory storage until database is available")

# Health check
@app.get("/health")
async def health_check():
    """Simple health check endpoint"""
    return {"status": "healthy", "version": "1.0.0"}

# Include routers
app.include_router(auth.router)
app.include_router(projects.router)
app.include_router(datasets.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
