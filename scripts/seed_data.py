"""
Script to seed the database with sample genres and movies
Run this after creating your first admin user
"""
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal
from app.models.movie import Genre, Movie, MovieGenre
from app.models.user import User
from app.utils.security import get_password_hash


def seed_genres():
    """Create sample genres"""
    db = SessionLocal()
    
    genres_data = [
        {"name": "Action", "slug": "action"},
        {"name": "Adventure", "slug": "adventure"},
        {"name": "Comedy", "slug": "comedy"},
        {"name": "Drama", "slug": "drama"},
        {"name": "Horror", "slug": "horror"},
        {"name": "Science Fiction", "slug": "sci-fi"},
        {"name": "Thriller", "slug": "thriller"},
        {"name": "Romance", "slug": "romance"},
        {"name": "Animation", "slug": "animation"},
        {"name": "Documentary", "slug": "documentary"},
        {"name": "Fantasy", "slug": "fantasy"},
        {"name": "Mystery", "slug": "mystery"},
    ]
    
    print("🎬 Creating genres...")
    created_count = 0
    
    for genre_data in genres_data:
        # Check if genre already exists
        existing = db.query(Genre).filter(Genre.slug == genre_data["slug"]).first()
        if not existing:
            genre = Genre(**genre_data)
            db.add(genre)
            created_count += 1
            print(f"  ✓ Created genre: {genre_data['name']}")
        else:
            print(f"  ⊙ Genre already exists: {genre_data['name']}")
    
    db.commit()
    db.close()
    print(f"✅ Created {created_count} new genres\n")


def seed_admin_user():
    """Create an admin user if not exists"""
    db = SessionLocal()
    
    # Check if admin exists
    admin = db.query(User).filter(User.username == "admin").first()
    
    if not admin:
        print("👤 Creating admin user...")
        admin = User(
            username="admin",
            email="admin@example.com",
            password_hash=get_password_hash("admin123"),
            full_name="Admin User",
            is_active=True,
            is_admin=True
        )
        db.add(admin)
        db.commit()
        print("✅ Admin user created")
        print("   Username: admin")
        print("   Password: admin123")
        print("   ⚠️  CHANGE THIS PASSWORD IN PRODUCTION!\n")
    else:
        print("⊙ Admin user already exists\n")
    
    db.close()


def seed_sample_movies():
    """Create sample movies"""
    db = SessionLocal()
    
    # Get genres
    action = db.query(Genre).filter(Genre.slug == "action").first()
    sci_fi = db.query(Genre).filter(Genre.slug == "sci-fi").first()
    drama = db.query(Genre).filter(Genre.slug == "drama").first()
    comedy = db.query(Genre).filter(Genre.slug == "comedy").first()
    
    if not all([action, sci_fi, drama, comedy]):
        print("⚠️  Please run seed_genres() first")
        db.close()
        return
    
    movies_data = [
        {
            "title": "The Great Adventure",
            "description": "An epic journey through unknown lands filled with danger and excitement.",
            "duration": 7200,  # 2 hours
            "release_year": 2023,
            "director": "John Director",
            "cast": '["Actor One", "Actor Two", "Actor Three"]',
            "rating": "PG-13",
            "language": "English",
            "country": "USA",
            "status": "ready",
            "is_featured": True,
            "is_trending": True,
            "genres": [action.id, sci_fi.id]
        },
        {
            "title": "Comedy Night",
            "description": "A hilarious comedy that will make you laugh until you cry.",
            "duration": 5400,  # 1.5 hours
            "release_year": 2024,
            "director": "Jane Funny",
            "cast": '["Comedian One", "Comedian Two"]',
            "rating": "PG",
            "language": "English",
            "country": "USA",
            "status": "ready",
            "is_featured": False,
            "is_trending": True,
            "genres": [comedy.id]
        },
        {
            "title": "Dramatic Story",
            "description": "A powerful drama about life, love, and loss.",
            "duration": 8100,  # 2.25 hours
            "release_year": 2023,
            "director": "Drama Master",
            "cast": '["Serious Actor", "Dramatic Actress"]',
            "rating": "R",
            "language": "English",
            "country": "USA",
            "status": "ready",
            "is_featured": True,
            "is_trending": False,
            "genres": [drama.id]
        },
        {
            "title": "Space Odyssey",
            "description": "Journey to the far reaches of space in this thrilling sci-fi adventure.",
            "duration": 9000,  # 2.5 hours
            "release_year": 2024,
            "director": "Sci-Fi Director",
            "cast": '["Space Hero", "Alien Friend"]',
            "rating": "PG-13",
            "language": "English",
            "country": "USA",
            "status": "ready",
            "is_featured": True,
            "is_trending": True,
            "genres": [sci_fi.id, action.id]
        },
    ]
    
    print("🎥 Creating sample movies...")
    created_count = 0
    
    for movie_data in movies_data:
        # Check if movie exists
        existing = db.query(Movie).filter(Movie.title == movie_data["title"]).first()
        
        if not existing:
            genre_ids = movie_data.pop("genres")
            movie = Movie(**movie_data)
            db.add(movie)
            db.flush()
            
            # Add genres
            for genre_id in genre_ids:
                movie_genre = MovieGenre(movie_id=movie.id, genre_id=genre_id)
                db.add(movie_genre)
            
            created_count += 1
            print(f"  ✓ Created movie: {movie_data['title']}")
        else:
            print(f"  ⊙ Movie already exists: {movie_data['title']}")
    
    db.commit()
    db.close()
    print(f"✅ Created {created_count} new movies\n")


def main():
    """Run all seed functions"""
    print("=" * 60)
    print("🌱 SEEDING DATABASE")
    print("=" * 60 + "\n")
    
    seed_admin_user()
    seed_genres()
    seed_sample_movies()
    
    print("=" * 60)
    print("✅ DATABASE SEEDING COMPLETE!")
    print("=" * 60)
    print("\n📝 Next steps:")
    print("1. Start the server: python -m app.main")
    print("2. Login as admin at: http://localhost:8000/docs")
    print("3. Test the movie endpoints")
    print("\n")


if __name__ == "__main__":
    main()