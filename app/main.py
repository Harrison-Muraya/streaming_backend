from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def read_root():
    return {"Hello": "World"}

# Authentication Routes

@app.post("/api/v1/auth/register")
async def register_user():
    return {"message": "User registered successfully"}

# Login Route
@app.post("/api/v1/auth/login")
async def login_user():
    return {"message": "User logged in successfully"}   

# Token Refresh Route
@app.post("/api/v1/auth/refresh ")
async def refresh_token():
    return {"message": "Token refreshed successfully"}

# Logout Route
@app.post("/api/v1/auth/logout")
async def logout_user():
    return {"message": "User logged out successfully"} 

# Get Current User Route
@app.get("/api/v1/auth/me") 
async def get_current_user():
    return {"message": "Current user details"}
