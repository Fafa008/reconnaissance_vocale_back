from fastapi import APIRouter, UploadFile, File
from app.services.transcriber import transcribe_audio

router = APIRouter()

@router.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    return await transcribe_audio(file)

@router.get("/health")
async def health():
    return {"status": "ok"}