"""
Script to test Movie API endpoints
Run this from the project root:
    python test_api.py
"""
import requests
import json
import sys

BASE_URL = "http://localhost:8000/api/v1"


def check_server():
    """Check if server is running"""
    try:
        response = requests.get("http://localhost:8000/health", timeout=2)
        if response.status_code == 200:
            return True
    except:
        pass
    return False


def login_as_admin():
    """Login and get access token"""
    print("🔐 Logging in as admin...")
    try:
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
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def test_get_genres(token):
    """Test getting all genres"""
    print("📂 Testing: GET /movies/genres")
    try:
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
    except Exception as e:
        print(f"❌ Error: {e}\n")
        return []


def test_get_movies(token):
    """Test getting movies with pagination"""
    print("🎬 Testing: GET /movies (with pagination)")
    try:
        response = requests.get(
            f"{BASE_URL}/movies",
            params={"page": 1, "page_size": 10}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Found {data['total']} total movies")
            print(f"   Page {data['page']} of {data['total_pages']}")
            print(f"   Showing {len(data['movies'])} movies")
            if data['movies']:
                print(f"   First movie: {data['movies'][0]['title']}")
            print()
            return data['movies']
        else:
            print(f"❌ Failed: {response.text}\n")
            return []
    except Exception as e:
        print(f"❌ Error: {e}\n")
        return []


def test_search_movies(token):
    """Test searching movies"""
    print("🔍 Testing: Search movies")
    try:
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
    except Exception as e:
        print(f"❌ Error: {e}\n")


def test_featured_movies(token):
    """Test getting featured movies"""
    print("⭐ Testing: GET /movies/collections/featured")
    try:
        response = requests.get(f"{BASE_URL}/movies/collections/featured")
        
        if response.status_code == 200:
            movies = response.json()
            print(f"✅ Featured movies: {len(movies)}")
            for movie in movies:
                print(f"   - {movie['title']}")
            print()
        else:
            print(f"❌ Failed: {response.text}\n")
    except Exception as e:
        print(f"❌ Error: {e}\n")


def main():
    """Run all tests"""
    print("=" * 60)
    print("🧪 TESTING MOVIE API")
    print("=" * 60 + "\n")
    
    # Check if server is running
    if not check_server():
        print("❌ Server is not running!")
        print("\nPlease start the server first:")
        print("  python -m app.main")
        print("\nThen run this script again.")
        sys.exit(1)
    
    print("✅ Server is running\n")
    
    # Login
    token = login_as_admin()
    if not token:
        print("\n❌ Cannot proceed without authentication")
        print("\nMake sure you've run the seed script:")
        print("  python seed_data.py")
        sys.exit(1)
    
    # Test endpoints
    genres = test_get_genres(token)
    movies = test_get_movies(token)
    test_search_movies(token)
    test_featured_movies(token)
    
    print("=" * 60)
    print("✅ ALL TESTS COMPLETE!")
    print("=" * 60 + "\n")
    
    if not movies:
        print("⚠️  No movies found in database")
        print("Run the seed script to add sample data:")
        print("  python seed_data.py\n")


if __name__ == "__main__":
    main()