"""
GutSense FastAPI Backend
A gut-based personalized food advisor using rule-based logic
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.database import engine, Base
from app.routers import auth, gut_profile, food_analysis
from app.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Create database tables
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created")
    yield
    print("🔄 Application shutting down")


# Create FastAPI app
app = FastAPI(
    title="GutSense API",
    description="AI-powered gut health food advisor",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "*"],  # Add your frontend URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(gut_profile.router, prefix="/api/gut-profile", tags=["Gut Profile"])
app.include_router(food_analysis.router, prefix="/api/food", tags=["Food Analysis"])


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "🦠 GutSense API is running!",
        "version": "1.0.0",
        "status": "healthy"
    }


@app.get("/api/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "database": "connected",
        "version": "1.0.0"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )