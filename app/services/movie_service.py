from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_, func
from fastapi import HTTPException, status
from app.models.movie import Movie, Genre, MovieGenre, VideoFile
from app.schemas.movie import MovieCreate, MovieUpdate
import math


class MovieService:
    """Service for movie-related operations"""
    
    @staticmethod
    def create_movie(movie_data: MovieCreate, db: Session) -> Movie:
        """Create a new movie"""
        # Create movie
        new_movie = Movie(
            title=movie_data.title,
            description=movie_data.description,
            duration=movie_data.duration,
            release_year=movie_data.release_year,
            director=movie_data.director,
            cast=movie_data.cast,
            rating=movie_data.rating,
            language=movie_data.language,
            country=movie_data.country,
            poster_url=movie_data.poster_url,
            backdrop_url=movie_data.backdrop_url,
            trailer_url=movie_data.trailer_url,
            status="pending"
        )
        
        db.add(new_movie)
        db.flush()  # Get the ID without committing
        
        # Add genres
        if movie_data.genre_ids:
            for genre_id in movie_data.genre_ids:
                # Verify genre exists
                genre = db.query(Genre).filter(Genre.id == genre_id).first()
                if not genre:
                    db.rollback()
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Genre with id {genre_id} not found"
                    )
                
                movie_genre = MovieGenre(movie_id=new_movie.id, genre_id=genre_id)
                db.add(movie_genre)
        
        db.commit()
        db.refresh(new_movie)
        return new_movie
    
    @staticmethod
    def get_movie_by_id(movie_id: int, db: Session) -> Movie:
        """Get movie by ID"""
        movie = db.query(Movie).filter(Movie.id == movie_id).first()
        if not movie:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Movie with id {movie_id} not found"
            )
        return movie
    
    @staticmethod
    def get_movies(
        db: Session,
        skip: int = 0,
        limit: int = 20,
        search: Optional[str] = None,
        genre_id: Optional[int] = None,
        status: Optional[str] = None,
        is_featured: Optional[bool] = None,
        is_trending: Optional[bool] = None,
        release_year: Optional[int] = None
    ) -> tuple[List[Movie], int]:
        """Get movies with filters and pagination"""
        query = db.query(Movie)
        
        # Apply filters
        if search:
            search_term = f"%{search}%"
            query = query.filter(
                or_(
                    Movie.title.ilike(search_term),
                    Movie.description.ilike(search_term),
                    Movie.director.ilike(search_term),
                    Movie.cast.ilike(search_term)
                )
            )
        
        if genre_id:
            query = query.join(MovieGenre).filter(MovieGenre.genre_id == genre_id)
        
        if status:
            query = query.filter(Movie.status == status)
        
        if is_featured is not None:
            query = query.filter(Movie.is_featured == is_featured)
        
        if is_trending is not None:
            query = query.filter(Movie.is_trending == is_trending)
        
        if release_year:
            query = query.filter(Movie.release_year == release_year)
        
        # Get total count
        total = query.count()
        
        # Apply pagination and ordering
        movies = query.order_by(Movie.created_at.desc()).offset(skip).limit(limit).all()
        
        return movies, total
    
    @staticmethod
    def update_movie(movie_id: int, movie_update: MovieUpdate, db: Session) -> Movie:
        """Update movie information"""
        movie = MovieService.get_movie_by_id(movie_id, db)
        
        # Update fields if provided
        update_data = movie_update.model_dump(exclude_unset=True)
        
        # Handle genre updates separately
        genre_ids = update_data.pop('genre_ids', None)
        
        # Update other fields
        for field, value in update_data.items():
            setattr(movie, field, value)
        
        # Update genres if provided
        if genre_ids is not None:
            # Remove existing genres
            db.query(MovieGenre).filter(MovieGenre.movie_id == movie_id).delete()
            
            # Add new genres
            for genre_id in genre_ids:
                genre = db.query(Genre).filter(Genre.id == genre_id).first()
                if not genre:
                    db.rollback()
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Genre with id {genre_id} not found"
                    )
                
                movie_genre = MovieGenre(movie_id=movie_id, genre_id=genre_id)
                db.add(movie_genre)
        
        db.commit()
        db.refresh(movie)
        return movie
    
    @staticmethod
    def delete_movie(movie_id: int, db: Session) -> None:
        """Delete a movie"""
        movie = MovieService.get_movie_by_id(movie_id, db)
        db.delete(movie)
        db.commit()
    
    @staticmethod
    def increment_view_count(movie_id: int, db: Session) -> None:
        """Increment movie view count"""
        movie = MovieService.get_movie_by_id(movie_id, db)
        movie.view_count += 1
        db.commit()


class GenreService:
    """Service for genre-related operations"""
    
    @staticmethod
    def create_genre(name: str, slug: str, db: Session) -> Genre:
        """Create a new genre"""
        # Check if genre already exists
        existing = db.query(Genre).filter(
            or_(Genre.name == name, Genre.slug == slug)
        ).first()
        
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Genre with this name or slug already exists"
            )
        
        genre = Genre(name=name, slug=slug)
        db.add(genre)
        db.commit()
        db.refresh(genre)
        return genre
    
    @staticmethod
    def get_all_genres(db: Session) -> List[Genre]:
        """Get all genres"""
        return db.query(Genre).order_by(Genre.name).all()
    
    @staticmethod
    def get_genre_by_id(genre_id: int, db: Session) -> Genre:
        """Get genre by ID"""
        genre = db.query(Genre).filter(Genre.id == genre_id).first()
        if not genre:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Genre with id {genre_id} not found"
            )
        return genre
    
    @staticmethod
    def get_genre_by_slug(slug: str, db: Session) -> Genre:
        """Get genre by slug"""
        genre = db.query(Genre).filter(Genre.slug == slug).first()
        if not genre:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Genre with slug '{slug}' not found"
            )
        return genre
    
    @staticmethod
    def delete_genre(genre_id: int, db: Session) -> None:
        """Delete a genre"""
        genre = GenreService.get_genre_by_id(genre_id, db)
        db.delete(genre)
        db.commit()