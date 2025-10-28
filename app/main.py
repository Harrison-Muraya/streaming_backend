from fastapi import FastAPI
from app.routers import auth, movies, straming, recommendations, admin
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.config import settings
from app.database import create_tables
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

# Mount static files (for serving videos if using local storage)
if os.path.exists(settings.MEDIA_ROOT):
    app.mount("/media", StaticFiles(directory=settings.MEDIA_ROOT), name="media")


# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize app on startup"""
    print("🚀 Starting Streaming API...")
    create_tables()
    print("✅ Database tables created/verified")
    print(f"✅ Server running on http://{settings.HOST}:{settings.PORT}")


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    print("👋 Shutting down Streaming API...")


# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Welcome to Streaming API",
        "version": settings.VERSION,
        "docs": "/docs",
        "redoc": "/redoc"
    }


# Health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "version": settings.VERSION
    }

# Include route groups
app.include_router(auth.router)
app.include_router(movies.router)
app.include_router(straming.router)
app.include_router(recommendations.router)
app.include_router(admin.router)


# Run the app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
