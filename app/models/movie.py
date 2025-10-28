from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, BigInteger
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Genre(Base):
    __tablename__ = "genres"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    slug = Column(String(50), unique=True, nullable=False)
    
    # Relationships
    movie_genres = relationship("MovieGenre", back_populates="genre")
    
    def __repr__(self):
        return f"<Genre {self.name}>"


class Movie(Base):
    __tablename__ = "movies"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text)
    duration = Column(Integer)  # in seconds
    release_year = Column(Integer)
    director = Column(String(100))
    cast = Column(Text)  # JSON string of actors
    rating = Column(String(10))  # PG, PG-13, R, etc.
    language = Column(String(50), default="English")
    country = Column(String(50))
    
    # File information
    poster_url = Column(String(500))
    backdrop_url = Column(String(500))
    trailer_url = Column(String(500))
    video_url = Column(String(500))  # Primary video URL
    original_filename = Column(String(255))
    
    # Status tracking
    status = Column(String(50), default="pending")  # pending, processing, ready, failed
    upload_progress = Column(Integer, default=0)
    
    # Metadata
    view_count = Column(Integer, default=0)
    is_featured = Column(Boolean, default=False)
    is_trending = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    genres = relationship("MovieGenre", back_populates="movie", cascade="all, delete-orphan")
    video_files = relationship("VideoFile", back_populates="movie", cascade="all, delete-orphan")
    conversion_jobs = relationship("ConversionJob", back_populates="movie", cascade="all, delete-orphan")
    watch_history = relationship("WatchHistory", back_populates="movie", cascade="all, delete-orphan")
    ratings = relationship("MovieRating", back_populates="movie", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Movie {self.title}>"


class MovieGenre(Base):
    __tablename__ = "movie_genres"
    
    id = Column(Integer, primary_key=True, index=True)
    movie_id = Column(Integer, ForeignKey("movies.id", ondelete="CASCADE"), nullable=False)
    genre_id = Column(Integer, ForeignKey("genres.id", ondelete="CASCADE"), nullable=False)
    
    # Relationships
    movie = relationship("Movie", back_populates="genres")
    genre = relationship("Genre", back_populates="movie_genres")
    
    def __repr__(self):
        return f"<MovieGenre movie_id={self.movie_id} genre_id={self.genre_id}>"


class VideoFile(Base):
    __tablename__ = "video_files"
    
    id = Column(Integer, primary_key=True, index=True)
    movie_id = Column(Integer, ForeignKey("movies.id", ondelete="CASCADE"), nullable=False)
    quality = Column(String(20), nullable=False)  # 1080p, 720p, 480p, 360p
    file_path = Column(String(500), nullable=False)
    file_size = Column(BigInteger)  # in bytes
    codec = Column(String(50))
    bitrate = Column(Integer)  # in kbps
    resolution_width = Column(Integer)
    resolution_height = Column(Integer)
    format_type = Column(String(20))  # mp4, hls, dash
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    movie = relationship("Movie", back_populates="video_files")
    
    def __repr__(self):
        return f"<VideoFile movie_id={self.movie_id} quality={self.quality}>"


class ConversionJob(Base):
    __tablename__ = "conversion_jobs"
    
    id = Column(Integer, primary_key=True, index=True)
    movie_id = Column(Integer, ForeignKey("movies.id", ondelete="CASCADE"), nullable=False)
    status = Column(String(50), default="queued")  # queued, processing, completed, failed
    progress = Column(Integer, default=0)  # 0-100
    current_step = Column(String(100))  # e.g., "Converting to 1080p", "Generating thumbnails"
    error_message = Column(Text)
    task_id = Column(String(255))  # Celery task ID
    started_at = Column(DateTime)
    completed_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    movie = relationship("Movie", back_populates="conversion_jobs")
    
    def __repr__(self):
        return f"<ConversionJob movie_id={self.movie_id} status={self.status}>"