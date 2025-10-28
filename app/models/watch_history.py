from sqlalchemy import Column, Integer, Float, Boolean, DateTime, ForeignKey, UniqueConstraint, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class WatchHistory(Base):
    __tablename__ = "watch_history"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    movie_id = Column(Integer, ForeignKey("movies.id", ondelete="CASCADE"), nullable=False)
    watch_percentage = Column(Float, default=0.0)  # 0.0 to 100.0
    last_position = Column(Integer, default=0)  # in seconds
    completed = Column(Boolean, default=False)
    watched_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="watch_history")
    movie = relationship("Movie", back_populates="watch_history")
    
    # Ensure unique combination of user and movie
    __table_args__ = (
        UniqueConstraint('user_id', 'movie_id', name='unique_user_movie_watch'),
    )
    
    def __repr__(self):
        return f"<WatchHistory user_id={self.user_id} movie_id={self.movie_id}>"


class MovieRating(Base):
    __tablename__ = "movie_ratings"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    movie_id = Column(Integer, ForeignKey("movies.id", ondelete="CASCADE"), nullable=False)
    rating = Column(Integer, nullable=False)  # 1-5 stars
    review = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="ratings")
    movie = relationship("Movie", back_populates="ratings")
    
    # Ensure unique combination of user and movie
    __table_args__ = (
        UniqueConstraint('user_id', 'movie_id', name='unique_user_movie_rating'),
    )
    
    def __repr__(self):
        return f"<MovieRating user_id={self.user_id} movie_id={self.movie_id} rating={self.rating}>"