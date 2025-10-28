"""
Quick script to verify your models and database setup
Run: python verify_setup.py
"""
import sys

print("🔍 Verifying FastAPI Setup...\n")

# Test 1: Import models
print("1️⃣ Testing model imports...")
try:
    from app.models.movie import Movie, Genre, MovieGenre, VideoFile, ConversionJob
    from app.models.user import User
    from app.models.watch_history import WatchHistory, MovieRating
    print("   ✅ All models imported successfully\n")
except Exception as e:
    print(f"   ❌ Error importing models: {e}\n")
    sys.exit(1)

# Test 2: Check database connection
print("2️⃣ Testing database connection...")
try:
    from app.database import SessionLocal, engine
    from sqlalchemy import text
    
    db = SessionLocal()
    result = db.execute(text("SELECT 1"))
    db.close()
    print("   ✅ Database connection successful\n")
except Exception as e:
    print(f"   ❌ Database connection failed: {e}")
    print("   Make sure PostgreSQL is running and .env is configured correctly\n")
    sys.exit(1)

# Test 3: Check table creation
print("3️⃣ Creating/verifying database tables...")
try:
    from app.database import Base
    Base.metadata.create_all(bind=engine)
    print("   ✅ All tables created/verified\n")
except Exception as e:
    print(f"   ❌ Error creating tables: {e}\n")
    sys.exit(1)

# Test 4: Verify relationships
print("4️⃣ Verifying model relationships...")
try:
    # Check Movie model has correct attributes
    assert hasattr(Movie, 'movie_genres'), "Movie missing movie_genres relationship"
    assert hasattr(Movie, 'genres'), "Movie missing genres property"
    
    # Check Genre model
    assert hasattr(Genre, 'movie_genres'), "Genre missing movie_genres relationship"
    
    # Check MovieGenre model
    assert hasattr(MovieGenre, 'movie'), "MovieGenre missing movie relationship"
    assert hasattr(MovieGenre, 'genre'), "MovieGenre missing genre relationship"
    
    print("   ✅ All relationships configured correctly\n")
except AssertionError as e:
    print(f"   ❌ Relationship error: {e}\n")
    sys.exit(1)

# Test 5: Test creating a sample object
print("5️⃣ Testing model instantiation...")
try:
    db = SessionLocal()
    
    # Check if admin user exists
    admin = db.query(User).filter(User.username == "admin").first()
    if admin:
        print(f"   ✅ Admin user found: {admin.username}")
    else:
        print("   ⚠️  No admin user found (run seed_data.py to create)")
    
    # Check genres
    genre_count = db.query(Genre).count()
    print(f"   ✅ Genres in database: {genre_count}")
    
    # Check movies
    movie_count = db.query(Movie).count()
    print(f"   ✅ Movies in database: {movie_count}")
    
    db.close()
    print()
except Exception as e:
    print(f"   ❌ Error: {e}\n")
    sys.exit(1)

# Test 6: Test genre property
print("6️⃣ Testing Movie.genres property...")
try:
    db = SessionLocal()
    movie = db.query(Movie).first()
    
    if movie:
        # This should not raise an error
        genres = movie.genres
        print(f"   ✅ Movie '{movie.title}' has {len(genres)} genres")
        if genres:
            print(f"   ✅ First genre: {genres[0].name}")
    else:
        print("   ⚠️  No movies in database to test (run seed_data.py)")
    
    db.close()
    print()
except Exception as e:
    print(f"   ❌ Error accessing genres property: {e}\n")
    sys.exit(1)

# Summary
print("=" * 60)
print("✅ ALL CHECKS PASSED!")
print("=" * 60)
print("\n📝 Your setup is ready! You can now:")
print("1. Start the server: python -m app.main")
print("2. Access API docs: http://localhost:8000/docs")
print("3. Test endpoints: python test_api.py")
print("\n")