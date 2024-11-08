from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import text_router, image_router

app = FastAPI()

# Configure CORS with more specific settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Specifically allow React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Add a test endpoint
@app.get("/")
async def root():
    return {"message": "Server is running"}

# Include routers
app.include_router(text_router.router, prefix="/api")
app.include_router(image_router.router, prefix="/api")