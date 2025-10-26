from fastapi import APIRouter, Depends, HTTPException

router = APIRouter(prefix="/api/v1", tags=["Streaming"])

# Streaming Endpoints
# Start Streaming Route
@router.get("/stream/{movie_id}")
async def start_streaming(movie_id: int):
    return {"message": f"Streaming started for movie with id {movie_id}"}

# watch progress update route
@router.post("/watch/progress")
async def update_watch_progress(movie_id: int, progress: float):
    return {"message": f"Watch progress for movie id {movie_id} updated to {progress}%"}

# Get Watch History Route
@router.get("/watch/history")
async def get_watch_history():
    return {"message": "User watch history"}
