import pandas as pd
from pathlib import Path
from core.config import UPLOAD_DIR, ALLOWED_EXTENSIONS
from fastapi import UploadFile, HTTPException

class DataService:
    @staticmethod
    async def save_file(file: UploadFile) -> str:
        # Check file extension
        file_extension = Path(file.filename).suffix.lower()
        if file_extension not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"File type not allowed. Allowed types: {ALLOWED_EXTENSIONS}"
            )
        
        # Save file
        file_path = UPLOAD_DIR / file.filename
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        return file.filename

    @staticmethod
    def read_file(filename: str) -> dict:
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