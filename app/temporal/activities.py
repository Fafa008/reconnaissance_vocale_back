import asyncio
import os
from temporalio import activity
from .shared_types import TranscriptionParams, TranscriptionResult
from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC
import torch
import soundfile as sf

# Chargement global (au niveau du module)
MODEL_NAME = "jonatasgrosman/wav2vec2-large-xlsr-53-french"
print("Chargement du modèle (une seule fois)...")
processor = Wav2Vec2Processor.from_pretrained(MODEL_NAME)
model = Wav2Vec2ForCTC.from_pretrained(MODEL_NAME)
model.eval()
print("Modèle ASR chargé globalement")

class InvalidAudioError(Exception):
    pass

@activity.defn(name="transcribe_audio_activity")
async def transcribe_audio(params: TranscriptionParams) -> TranscriptionResult:
    def sync_transcription():
        # Vérifier que le fichier existe
        if not os.path.exists(params.file_path):
            raise FileNotFoundError(f"Fichier introuvable : {params.file_path}")
        audio_input, sample_rate = sf.read(params.file_path)
        # Resampling si nécessaire
        if sample_rate != 16000:
            import librosa
            audio_input = librosa.resample(audio_input, orig_sr=sample_rate, target_sr=16000)
        inputs = processor(audio_input, sampling_rate=16000, return_tensors="pt", padding=True)
        with torch.no_grad():
            logits = model(**inputs).logits
        predicted_ids = torch.argmax(logits, dim=-1)
        transcription = processor.batch_decode(predicted_ids)[0]
        # Nettoyer le fichier temporaire
        os.unlink(params.file_path)
        return transcription.lower().strip()

    text = await asyncio.to_thread(sync_transcription)
    return TranscriptionResult(text=text)