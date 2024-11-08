from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..services.text_service import TextService

router = APIRouter()
text_service = TextService()

class TextRequest(BaseModel):
    text: str
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "text": "Sample text to process."
                }
            ]
        }
    }

class TextResponse(BaseModel):
    processed_text: str
    tokens: str
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "processed_text": "processed sample text",
                    "tokens": "sample tokens"
                }
            ]
        }
    }

@router.post("/process-text", response_model=TextResponse)
async def process_text(request: TextRequest):
    try:
        result = text_service.process_text(request.text)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/augment-text")
async def augment_text(request: TextRequest):
    try:
        augmented_text = text_service.augment_text(request.text)
        return {"augmented_text": augmented_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 