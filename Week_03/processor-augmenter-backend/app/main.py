from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import text_router

app = FastAPI()

# Configure CORS with more permissive settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins during development
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add a test endpoint
@app.get("/")
async def root():
    return {"message": "Server is running"}

# Include routers
app.include_router(text_router.router, prefix="/api")