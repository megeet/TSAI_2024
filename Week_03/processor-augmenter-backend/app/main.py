from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import text_router

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(text_router.router, prefix="/api") 