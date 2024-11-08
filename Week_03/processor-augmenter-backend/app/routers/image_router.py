from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import Response, JSONResponse
from ..services.image_service import ImageService
import base64
import io

router = APIRouter()
image_service = ImageService()

def bytes_to_base64(bytes_data):
    return base64.b64encode(bytes_data).decode('utf-8')

@router.post("/process-image")
async def process_image(image: UploadFile = File(...)):
    try:
        contents = await image.read()
        processed_image = image_service.process_image(contents)
        return Response(content=processed_image, media_type="image/png")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/augment-image")
async def augment_image(image: UploadFile = File(...)):
    try:
        contents = await image.read()
        augmented_images = image_service.augment_image(contents)
        
        # Convert bytes to base64 strings
        response_data = {
            "adjusted": f"data:image/png;base64,{bytes_to_base64(augmented_images['adjusted'])}",
            "flipped": f"data:image/png;base64,{bytes_to_base64(augmented_images['flipped'])}"
        }
        
        return JSONResponse(content=response_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 