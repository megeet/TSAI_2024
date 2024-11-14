from fastapi import APIRouter, UploadFile, File, HTTPException, Request
from pydantic import BaseModel
from ..services.model_service import ModelService
from typing import Dict, List
import json

router = APIRouter()
model_service = ModelService()

class ModelData(BaseModel):
    vertices: List[List[float]]
    faces: List[List[int]]

class ModelRequest(BaseModel):
    model_data: ModelData

@router.post("/upload-model")
async def upload_model(model: UploadFile = File(...)):
    try:
        contents = await model.read()
        model_data = model_service.load_off_file(contents)
        return {"model_data": model_data}
    except Exception as e:
        print(f"Upload error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/process-model")
async def process_model(request: Request):
    try:
        # Get raw request body
        body = await request.json()
        print("Received request body:", body)  # Debug print
        
        # Extract model data
        model_data = body.get('model_data')
        if not model_data or 'vertices' not in model_data or 'faces' not in model_data:
            raise ValueError("Invalid model data format")
            
        print("Processing model with vertices:", len(model_data['vertices']), "faces:", len(model_data['faces']))
        
        processed_model = model_service.process_model(model_data)
        print("Model processed successfully")
        
        return {"processed_model": processed_model}
    except Exception as e:
        print(f"Processing error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/augment-model")
async def augment_model(request: Request):
    try:
        # Get raw request body
        body = await request.json()
        print("Received request body:", body)  # Debug print
        
        # Extract model data
        model_data = body.get('model_data')
        if not model_data or 'vertices' not in model_data or 'faces' not in model_data:
            raise ValueError("Invalid model data format")
            
        print("Augmenting model with vertices:", len(model_data['vertices']), "faces:", len(model_data['faces']))
        
        augmented_model = model_service.augment_model(model_data)
        print("Model augmented successfully")
        
        return {"augmented_model": augmented_model}
    except Exception as e:
        print(f"Augmentation error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) 