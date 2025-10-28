from typing import Optional, List
from fastapi import APIRouter, Depends, Query, status, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.movie import (
    MovieCreate, MovieUpdate, MovieResponse, MovieList,
    GenreCreate, GenreResponse
)
from app.services.movie_service import MovieService, GenreService
from app.utils.security import get_current_active_user, require_admin
from app.models.user import User
import math

router = APIRouter()


# ============================================
# MOVIE ENDPOINTS
# ============================================

@router.post("/", response_model=MovieResponse, status_code=status.HTTP_201_CREATED)
async def create_movie(
    movie_data: MovieCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    Create a new movie (Admin only)
    
    - **title**: Movie title (required)
    - **description**: Movie description
    - **duration**: Duration in seconds
    - **release_year**: Year of release
    - **genre_ids**: List of genre IDs
    - **director**: Director name
    - **cast**: Cast information (JSON string)
    - **rating**: Content rating (PG, PG-13, R, etc.)
    """
    movie = MovieService.create_movie(movie_data, db)
    return movie


@router.get("/", response_model=MovieList)
async def get_movies(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    search: Optional[str] = Query(None, description="Search in title, description, director, cast"),
    genre_id: Optional[int] = Query(None, description="Filter by genre ID"),
    status: Optional[str] = Query(None, description="Filter by status (pending, processing, ready, failed)"),
    is_featured: Optional[bool] = Query(None, description="Filter featured movies"),
    is_trending: Optional[bool] = Query(None, description="Filter trending movies"),
    release_year: Optional[int] = Query(None, description="Filter by release year"),
    db: Session = Depends(get_db)
):
    """
    Get list of movies with pagination and filters
    
    All users can access this endpoint
    """
    skip = (page - 1) * page_size
    
    movies, total = MovieService.get_movies(
        db=db,
        skip=skip,
        limit=page_size,
        search=search,
        genre_id=genre_id,
        status=status,
        is_featured=is_featured,
        is_trending=is_trending,
        release_year=release_year
    )
    
    total_pages = math.ceil(total / page_size)
    
    return MovieList(
        movies=movies,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages
    )


@router.get("/{movie_id}", response_model=MovieResponse)
async def get_movie(
    movie_id: int,
    db: Session = Depends(get_db)
):
    """
    Get movie details by ID
    
    All users can access this endpoint
    """
    movie = MovieService.get_movie_by_id(movie_id, db)
    return movie


@router.put("/{movie_id}", response_model=MovieResponse)
async def update_movie(
    movie_id: int,
    movie_update: MovieUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    Update movie information (Admin only)
    
    Only provided fields will be updated
    """
    movie = MovieService.update_movie(movie_id, movie_update, db)
    return movie


@router.delete("/{movie_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_movie(
    movie_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    Delete a movie (Admin only)
    
    This will permanently delete the movie and all associated data
    """
    MovieService.delete_movie(movie_id, db)
    return None


@router.post("/{movie_id}/view", status_code=status.HTTP_200_OK)
async def increment_view_count(
    movie_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Increment view count for a movie
    
    Called when user starts watching a movie
    """
    MovieService.increment_view_count(movie_id, db)
    return {"message": "View count incremented"}


@router.get("/{movie_id}/stream")
async def get_stream_url(
    movie_id: int,
    quality: Optional[str] = Query("1080p", description="Video quality (1080p, 720p, 480p)"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get streaming URL for a movie
    
    Returns the appropriate video URL based on quality preference
    """
    movie = MovieService.get_movie_by_id(movie_id, db)
    
    # Check if movie is ready
    if movie.status != "ready":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Movie is not ready for streaming. Current status: {movie.status}"
        )
    
    # Get video file for requested quality
    from app.models.movie import VideoFile
    video_file = db.query(VideoFile).filter(
        VideoFile.movie_id == movie_id,
        VideoFile.quality == quality
    ).first()
    
    if not video_file:
        # Fallback to primary video URL
        if movie.video_url:
            return {
                "movie_id": movie_id,
                "title": movie.title,
                "stream_url": movie.video_url,
                "quality": "default",
                "format": "mp4"
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Video file not found for quality: {quality}"
            )
    
    return {
        "movie_id": movie_id,
        "title": movie.title,
        "stream_url": video_file.file_path,
        "quality": video_file.quality,
        "format": video_file.format_type,
        "file_size": video_file.file_size,
        "bitrate": video_file.bitrate
    }


# ============================================
# GENRE ENDPOINTS
# ============================================

@router.post("/genres", response_model=GenreResponse, status_code=status.HTTP_201_CREATED)
async def create_genre(
    genre_data: GenreCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    Create a new genre (Admin only)
    
    - **name**: Genre name
    - **slug**: URL-friendly slug
    """
    genre = GenreService.create_genre(genre_data.name, genre_data.slug, db)
    return genre


@router.get("/genres", response_model=List[GenreResponse])
async def get_genres(
    db: Session = Depends(get_db)
):
    """
    Get all genres
    
    All users can access this endpoint
    """
    genres = GenreService.get_all_genres(db)
    return genres


@router.get("/genres/{genre_id}", response_model=GenreResponse)
async def get_genre(
    genre_id: int,
    db: Session = Depends(get_db)
):
    """
    Get genre by ID
    """
    genre = GenreService.get_genre_by_id(genre_id, db)
    return genre


@router.get("/genres/slug/{slug}", response_model=GenreResponse)
async def get_genre_by_slug(
    slug: str,
    db: Session = Depends(get_db)
):
    """
    Get genre by slug
    """
    genre = GenreService.get_genre_by_slug(slug, db)
    return genre


@router.delete("/genres/{genre_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_genre(
    genre_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    Delete a genre (Admin only)
    """
    GenreService.delete_genre(genre_id, db)
    return None


@router.get("/genres/{genre_id}/movies", response_model=MovieList)
async def get_movies_by_genre(
    genre_id: int,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Get all movies in a specific genre
    """
    # Verify genre exists
    GenreService.get_genre_by_id(genre_id, db)
    
    skip = (page - 1) * page_size
    movies, total = MovieService.get_movies(
        db=db,
        skip=skip,
        limit=page_size,
        genre_id=genre_id
    )
    
    total_pages = math.ceil(total / page_size)
    
    return MovieList(
        movies=movies,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages
    )


# ============================================
# SPECIAL COLLECTIONS
# ============================================

@router.get("/collections/featured", response_model=List[MovieResponse])
async def get_featured_movies(
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """
    Get featured movies
    """
    movies, _ = MovieService.get_movies(
        db=db,
        skip=0,
        limit=limit,
        is_featured=True,
        status="ready"
    )
    return movies


@router.get("/collections/trending", response_model=List[MovieResponse])
async def get_trending_movies(
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """
    Get trending movies
    """
    movies, _ = MovieService.get_movies(
        db=db,
        skip=0,
        limit=limit,
        is_trending=True,
        status="ready"
    )
    return movies


@router.get("/collections/recent", response_model=List[MovieResponse])
async def get_recent_movies(
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """
    Get recently added movies
    """
    movies, _ = MovieService.get_movies(
        db=db,
        skip=0,
        limit=limit,
        status="ready"
    )
    return movies
