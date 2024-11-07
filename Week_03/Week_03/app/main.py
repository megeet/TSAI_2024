from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from api.endpoints import data
from pathlib import Path

app = FastAPI(title="Data Viewer")

# Mount static files directory
app.mount("/static", StaticFiles(directory=str(Path(__file__).parent / "static")), name="static")

# Include routers
app.include_router(data.router, prefix="/api", tags=["data"]) 