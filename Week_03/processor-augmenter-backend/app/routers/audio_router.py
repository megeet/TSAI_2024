from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import Response
from ..services.audio_service import AudioService

router = APIRouter()
audio_service = AudioService()

@router.post("/process-audio")
async def process_audio(audio: UploadFile = File(...)):
    try:
        contents = await audio.read()
        processed_audio = audio_service.process_audio(contents)
        return Response(content=processed_audio, media_type="audio/wav")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/augment-audio")
async def augment_audio(audio: UploadFile = File(...)):
    try:
        contents = await audio.read()
        augmented_audio = audio_service.augment_audio(contents)
        return Response(content=augmented_audio, media_type="audio/wav")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 