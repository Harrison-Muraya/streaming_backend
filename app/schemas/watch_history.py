from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class WatchProgressUpdate(BaseModel):
    movie_id: int
    last_position: int = Field(..., ge=0)  # in seconds
    watch_percentage: float = Field(..., ge=0.0, le=100.0)
    completed: bool = False


class WatchHistoryResponse(BaseModel):
    id: int
    user_id: int
    movie_id: int
    watch_percentage: float
    last_position: int
    completed: bool
    watched_at: datetime
    created_at: datetime
    
    class Config:
        from_attributes = True


class MovieRatingCreate(BaseModel):
    movie_id: int
    rating: int = Field(..., ge=1, le=5)
    review: Optional[str] = None


class MovieRatingResponse(BaseModel):
    id: int
    user_id: int
    movie_id: int
    rating: int
    review: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True