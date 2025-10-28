from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class GenreCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    slug: str = Field(..., min_length=1, max_length=50)


class GenreResponse(BaseModel):
    id: int
    name: str
    slug: str
    
    class Config:
        from_attributes = True


class VideoFileResponse(BaseModel):
    id: int
    quality: str
    file_path: str
    file_size: Optional[int]
    codec: Optional[str]
    bitrate: Optional[int]
    resolution_width: Optional[int]
    resolution_height: Optional[int]
    format_type: Optional[str]
    
    class Config:
        from_attributes = True


class ConversionJobResponse(BaseModel):
    id: int
    movie_id: int
    status: str
    progress: int
    current_step: Optional[str]
    error_message: Optional[str]
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    created_at: datetime
    
    class Config:
        from_attributes = True


class MovieCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    duration: Optional[int] = None  # in seconds
    release_year: Optional[int] = None
    director: Optional[str] = None
    cast: Optional[str] = None  # JSON string
    rating: Optional[str] = None
    language: str = "English"
    country: Optional[str] = None
    genre_ids: List[int] = []
    poster_url: Optional[str] = None
    backdrop_url: Optional[str] = None
    trailer_url: Optional[str] = None


class MovieUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    duration: Optional[int] = None
    release_year: Optional[int] = None
    director: Optional[str] = None
    cast: Optional[str] = None
    rating: Optional[str] = None
    language: Optional[str] = None
    country: Optional[str] = None
    genre_ids: Optional[List[int]] = None
    poster_url: Optional[str] = None
    backdrop_url: Optional[str] = None
    trailer_url: Optional[str] = None
    is_featured: Optional[bool] = None
    is_trending: Optional[bool] = None
    status: Optional[str] = None


class MovieResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    duration: Optional[int]
    release_year: Optional[int]
    director: Optional[str]
    cast: Optional[str]
    rating: Optional[str]
    language: str
    country: Optional[str]
    poster_url: Optional[str]
    backdrop_url: Optional[str]
    trailer_url: Optional[str]
    video_url: Optional[str]
    status: str
    view_count: int
    is_featured: bool
    is_trending: bool
    created_at: datetime
    updated_at: datetime
    genres: List[GenreResponse] = []
    video_files: List[VideoFileResponse] = []
    
    class Config:
        from_attributes = True


class MovieList(BaseModel):
    movies: List[MovieResponse]
    total: int
    page: int
    page_size: int
    total_pages: int