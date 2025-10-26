from fastapi import APIRouter, Depends, HTTPException

router = APIRouter(prefix="/api/v1/movies", tags=["Movies"])

# Movie Endpoints 
# Get All Movies Route
@router.get("/")
async def get_all_movies():
    return {"message": "List of all movies"}

# Get Movie by ID Route
@router.get("/{id}")
async def get_movie_by_id(id: int):
    return {"message": f"Details of movie with id {id}"}

# Search Movies Route
@router.get("/search")
async def search_movies(query: str):
    return {"message": f"Search results for query: {query}"}

# Get Movie Genres Route
@router.get("/genres")
async def get_movie_genres():
    return {"message": "List of movie genres"}

# Get Movies by Genre Route
@router.get("/genre/{id}")
async def get_movies():
    return {"message": "List of movies"}