from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def read_root():
    return {"Hello": "World"}

# Authentication Routes


# Movie Endpoints 
# Get All Movies Route
@app.get("/api/v1/movies")
async def get_all_movies():
    return {"message": "List of all movies"}

# Get Movie by ID Route
@app.get("/api/v1/movies/{id}")
async def get_movie_by_id(id: int):
    return {"message": f"Details of movie with id {id}"}

# Search Movies Route
@app.get("/api/v1/movies/search")
async def search_movies(query: str):
    return {"message": f"Search results for query: {query}"}

# Get Movie Genres Route
@app.get("/api/v1/movies/genres")
async def get_movie_genres():
    return {"message": "List of movie genres"}

# Get Movies by Genre Route
@app.get("/api/v1/movies/genre/{id}")
async def get_movies():
    return {"message": "List of movies"}

