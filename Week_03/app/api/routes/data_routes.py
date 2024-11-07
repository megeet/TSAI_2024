from fastapi import APIRouter, UploadFile, File
from services.data_service import DataService
from schemas.data_schemas import DataResponse
from typing import List

router = APIRouter()
data_service = DataService()

@router.post("/upload/", response_model=str)
async def upload_file(file: UploadFile = File(...)) -> str:
    """Upload a data file"""
    filename = await data_service.save_file(file)
    return filename

@router.get("/files/{filename}", response_model=DataResponse)
async def get_file_data(filename: str) -> DataResponse:
    """Get data from a specific file"""
    return data_service.read_file(filename) 