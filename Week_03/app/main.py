from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
import pandas as pd
from pathlib import Path
from typing import Dict, Any
import mimetypes
import logging

app = FastAPI(title="Multi-Format Viewer")

# Create necessary directories
UPLOAD_DIR = Path("app/static/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# Create subdirectories for different file types
(UPLOAD_DIR / "images").mkdir(exist_ok=True)
(UPLOAD_DIR / "audio").mkdir(exist_ok=True)
(UPLOAD_DIR / "models").mkdir(exist_ok=True)
(UPLOAD_DIR / "text").mkdir(exist_ok=True)

# Mount static files directory
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Configure templates
templates = Jinja2Templates(directory="app/templates")

# Define allowed file extensions
ALLOWED_EXTENSIONS = {
    'text': {'.txt', '.csv'},
    'image': {'.jpg', '.jpeg', '.png', '.gif'},
    'audio': {'.mp3', '.wav'},
    '3d': {'.glb', '.gltf', '.obj', '.off'}
}

# Configure logging
logging.basicConfig(level=logging.INFO)

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...), format: str = "text") -> Dict[str, Any]:
    """Upload a file and return appropriate response based on file type"""
    
    # Get file extension and check if it's allowed
    file_ext = Path(file.filename).suffix.lower()
    logging.info(f"Uploading file: {file.filename}, Format: {format}, Extension: {file_ext}")
    
    if file_ext not in ALLOWED_EXTENSIONS.get(format, set()):
        logging.error(f"File type not allowed: {file_ext} for format {format}")
        raise HTTPException(
            status_code=400, 
            detail=f"File type not allowed for {format} format"
        )
    
    # Determine the appropriate subdirectory
    subdir = {
        'text': 'text',
        'image': 'images',
        'audio': 'audio',
        '3d': 'models'
    }.get(format)
    
    file_path = UPLOAD_DIR / subdir / file.filename
    
    # Save the uploaded file
    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
    
    # Return appropriate response based on file type
    if format == 'text':
        if file_ext == '.csv':
            df = pd.read_csv(file_path)
            return {
                "filename": file.filename,
                "headers": df.columns.tolist(),
                "data": df.to_dict(orient="records")
            }
        else:  # .txt
            with open(file_path, 'r') as f:
                content = f.read()
            return {"content": content}
            
    else:  # image, audio, or 3D model
        # Get the mime type for the file
        mime_type, _ = mimetypes.guess_type(file_path)
        logging.info(f"File saved: {file_path}, MIME type: {mime_type}")
        
        # Return the URL path to the uploaded file
        relative_path = f"/static/uploads/{subdir}/{file.filename}"
        return {
            "url": relative_path,
            "mime_type": mime_type,
            "filename": file.filename
        }

@app.get("/files/{format}/{filename}")
async def get_file(format: str, filename: str):
    """Serve uploaded files"""
    subdir = {
        'text': 'text',
        'image': 'images',
        'audio': 'audio',
        '3d': 'models'
    }.get(format)
    
    if not subdir:
        raise HTTPException(status_code=400, detail="Invalid format")
    
    file_path = UPLOAD_DIR / subdir / filename
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(file_path)

# Optional: Add cleanup endpoint or automatic cleanup for old files
@app.on_event("startup")
async def startup_event():
    """Initialize mime types"""
    mimetypes.init()