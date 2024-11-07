from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import Dict, Any
import pandas as pd
from core.config import UPLOAD_DIR

router = APIRouter()

@router.post("/upload/")
async def upload_file(file: UploadFile = File(...)) -> Dict[str, str]:
    """Upload a data file"""
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed")
    
    file_path = UPLOAD_DIR / file.filename
    
    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
    
    return {"filename": file.filename}

@router.get("/data/{filename}")
async def get_data(filename: str) -> Dict[str, Any]:
    """Get data from a specific file"""
    file_path = UPLOAD_DIR / filename
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    
    try:
        df = pd.read_csv(file_path)
        return {
            "filename": filename,
            "headers": df.columns.tolist(),
            "data": df.to_dict(orient="records")
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error reading file: {str(e)}") 