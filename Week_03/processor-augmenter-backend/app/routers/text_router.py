from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..services.text_service import TextService

router = APIRouter()
text_service = TextService()

class TextRequest(BaseModel):
    text: str

@router.post("/process-text")
async def process_text(request: TextRequest):
    try:
        processed_text = text_service.process_text(request.text)
        return {"processed_text": processed_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/augment-text")
async def augment_text(request: TextRequest):
    try:
        augmented_text = text_service.augment_text(request.text)
        return {"augmented_text": augmented_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 