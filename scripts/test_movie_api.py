"""
Script to test Movie API endpoints
"""
import requests
import json

BASE_URL = "http://localhost:8000/api/v1"


def login_as_admin():
    """Login and get access token"""
    print("🔐 Logging in as admin...")
    response = requests.post(
        f"{BASE_URL}/auth/login",
        json={"username": "admin", "password": "admin123"}
    )
    
    if response.status_code == 200:
        token = response.json()["access_token"]
        print("✅ Login successful!\n")
        return token
    else:
        print(f"❌ Login failed: {response.text}")
        return None


def test_get_genres(token):
    """Test getting all genres"""
    print("📂 Testing: GET /movies/genres")
    response = requests.get(f"{BASE_URL}/movies/genres")
    
    if response.status_code == 200:
        genres = response.json()
        print(f"✅ Found {len(genres)} genres")
        for genre in genres[:3]:
            print(f"   - {genre['name']} ({genre['slug']})")
        print()
        return genres
    else:
        print(f"❌ Failed: {response.text}\n")
        return []


def test_get_movies(token):
    """Test getting movies with pagination"""
    print("🎬 Testing: GET /movies (with pagination)")
    response = requests.get(
        f"{BASE_URL}/movies",
        params={"page": 1, "page_size": 10}
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Found {data['total']} total movies")
        print(f"   Page {data['page']} of {data['total_pages']}")
        print(f"   Showing {len(data['movies'])} movies\n")
        return data['movies']
    else:
        print(f"❌ Failed: {response.text}\n")
        return []


def test_search_movies(token):
    """Test searching movies"""
    print("🔍 Testing: Search movies")
    response = requests.get(
        f"{BASE_URL}/movies",
        params={"search": "Space"}
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Search results: {data['total']} movies")
        for movie in data['movies']:
            print(f"   - {movie['title']}")
        print()
    else:
        print(f"❌ Failed: {response.text}\n")


def test_get_movie_details(token, movie_id):
    """Test getting movie details"""
    print(f"🎥 Testing: GET /movies/{movie_id}")
    response = requests.get(f"{BASE_URL}/movies/{movie_id}")
    
    if response.status_code == 200:
        movie = response.json()
        print(f"✅ Movie: {movie['title']}")
        print(f"   Duration: {movie['duration']} seconds")
        print(f"   Status: {movie['status']}")
        print(f"   Genres: {len(movie['genres'])}")
        print()
    else:
        print(f"❌ Failed: {response.text}\n")


def test_create_movie(token):
    """Test creating a new movie (admin only)"""
    print("➕ Testing: POST /movies (create movie)")
    headers = {"Authorization": f"Bearer {token}"}
    
    movie_data = {
        "title": "Test Movie via API",
        "description": "This is a test movie created via the API",
        "duration": 6000,
        "release_year": 2024,
        "director": "API Tester",
        "rating": "PG-13",
        "language": "English",
        "genre_ids": [1, 2]  # Assuming Action and Adventure
    }
    
    response = requests.post(
        f"{BASE_URL}/movies/",
        headers=headers,
        json=movie_data
    )
    
    if response.status_code == 201:
        movie = response.json()
        print(f"✅ Created movie: {movie['title']} (ID: {movie['id']})")
        print()
        return movie['id']
    else:
        print(f"❌ Failed: {response.text}\n")
        return None


def test_update_movie(token, movie_id):
    """Test updating a movie"""
    print(f"✏️  Testing: PUT /movies/{movie_id} (update movie)")
    headers = {"Authorization": f"Bearer {token}"}
    
    update_data = {
        "description": "Updated description via API test",
        "is_featured": True
    }
    
    response = requests.put(
        f"{BASE_URL}/movies/{movie_id}",
        headers=headers,
        json=update_data
    )
    
    if response.status_code == 200:
        movie = response.json()
        print(f"✅ Updated movie: {movie['title']}")
        print(f"   Featured: {movie['is_featured']}")
        print()
    else:
        print(f"❌ Failed: {response.text}\n")


def test_filter_by_genre(token, genre_id):
    """Test filtering movies by genre"""
    print(f"🎭 Testing: Filter movies by genre {genre_id}")
    response = requests.get(
        f"{BASE_URL}/movies/genres/{genre_id}/movies",
        params={"page": 1, "page_size": 10}
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Found {data['total']} movies in this genre")
        print()
    else:
        print(f"❌ Failed: {response.text}\n")


def test_featured_movies(token):
    """Test getting featured movies"""
    print("⭐ Testing: GET /movies/collections/featured")
    response = requests.get(f"{BASE_URL}/movies/collections/featured")
    
    if response.status_code == 200:
        movies = response.json()
        print(f"✅ Featured movies: {len(movies)}")
        for movie in movies:
            print(f"   - {movie['title']}")
        print()
    else:
        print(f"❌ Failed: {response.text}\n")


def test_trending_movies(token):
    """Test getting trending movies"""
    print("🔥 Testing: GET /movies/collections/trending")
    response = requests.get(f"{BASE_URL}/movies/collections/trending")
    
    if response.status_code == 200:
        movies = response.json()
        print(f"✅ Trending movies: {len(movies)}")
        for movie in movies:
            print(f"   - {movie['title']}")
        print()
    else:
        print(f"❌ Failed: {response.text}\n")


def main():
    """Run all tests"""
    print("=" * 60)
    print("🧪 TESTING MOVIE API")
    print("=" * 60 + "\n")
    
    # Login
    token = login_as_admin()
    if not token:
        print("Cannot proceed without authentication")
        return
    
    # Test genre endpoints
    genres = test_get_genres(token)
    
    # Test movie endpoints
    movies = test_get_movies(token)
    test_search_movies(token)
    
    if movies:
        test_get_movie_details(token, movies[0]['id'])
    
    # Test create and update (admin only)
    new_movie_id = test_create_movie(token)
    if new_movie_id:
        test_update_movie(token, new_movie_id)
    
    # Test filtering
    if genres:
        test_filter_by_genre(token, genres[0]['id'])
    
    # Test collections
    test_featured_movies(token)
    test_trending_movies(token)
    
    print("=" * 60)
    print("✅ ALL TESTS COMPLETE!")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()