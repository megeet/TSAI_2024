from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import Response, JSONResponse
from ..services.audio_service import AudioService
import base64

router = APIRouter()
audio_service = AudioService()

def bytes_to_base64(bytes_data):
    return base64.b64encode(bytes_data).decode('utf-8')

@router.post("/process-audio")
async def process_audio(audio: UploadFile = File(...)):
    try:
        contents = await audio.read()
        result = audio_service.process_audio(contents)
        
        return JSONResponse(content={
            "processed_audio": f"data:audio/wav;base64,{bytes_to_base64(result['processed_audio'])}",
            "mfcc_plot": f"data:image/png;base64,{bytes_to_base64(result['mfcc_plot'])}"
        })
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