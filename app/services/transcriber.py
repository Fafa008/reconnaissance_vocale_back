import io
import soundfile as sf
import librosa
import numpy as np
from fastapi import UploadFile, HTTPException
from app.models.asr import asr_model
from app.audio_utils import load_and_normalize   # car audio_utils.py est dans app/
from app.config import MAX_AUDIO_DURATION, SAMPLE_RATE

async def transcribe_audio(file: UploadFile):
    try:
        contents = await file.read()
        try:
            data, samplerate = sf.read(io.BytesIO(contents))
        except Exception:
            data, samplerate = librosa.load(io.BytesIO(contents), sr=None)
        
        audio_norm, new_sr = load_and_normalize(data, samplerate)
        
        max_len = MAX_AUDIO_DURATION * SAMPLE_RATE
        if len(audio_norm) > max_len:
            raise HTTPException(400, f"Audio trop long (max {MAX_AUDIO_DURATION}s)")
        
        text = asr_model.transcribe(audio_norm)
        return {"text": text, "status": "success"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, f"Erreur: {str(e)}")