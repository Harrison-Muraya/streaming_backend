from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.config import settings
from app.database import create_tables
from app.api.v1 import api_router
import os

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    debug=settings.DEBUG,
    description="Video Streaming API with ML Recommendations"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
if os.path.exists(settings.MEDIA_ROOT):
    app.mount("/media", StaticFiles(directory=settings.MEDIA_ROOT), name="media")


@app.on_event("startup")
async def startup_event():
    """Initialize app on startup"""
    print("🚀 Starting Streaming API...")
    create_tables()
    print("✅ Database tables created/verified")
    print(f"✅ Server running on http://{settings.HOST}:{settings.PORT}")
    print(f"📚 API Docs: http://{settings.HOST}:{settings.PORT}/docs")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    print("👋 Shutting down Streaming API...")


@app.get("/")
async def root():
    return {
        "message": "Welcome to Streaming API",
        "version": settings.VERSION,
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "version": settings.VERSION
    }


# Include API v1 router
app.include_router(api_router, prefix="/api/v1")



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )