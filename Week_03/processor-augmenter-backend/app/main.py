from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import text_router, image_router, audio_router

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Add routers
app.include_router(text_router.router, prefix="/api")
app.include_router(image_router.router, prefix="/api")
app.include_router(audio_router.router, prefix="/api")