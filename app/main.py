from fastapi import FastAPI
from app.routers import auth, movies, straming, recommendations, admin

app = FastAPI()

@app.get("/")
async def read_root():
    return {"Hello": "World"}

# Authentication Routes

# Include route groups
app.include_router(auth.router)
app.include_router(movies.router)
app.include_router(straming.router)
app.include_router(recommendations.router)
app.include_router(admin.router)


