import asyncio
from temporalio import activity
from .shared_types import TranscriptionParams, TranscriptionResult
from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC
import torch
import soundfile as sf

class InvalidAudioError(Exception):
    pass

@activity.defn(name="transcribe_audio_activity")
async def transcribe_audio(params: TranscriptionParams) -> TranscriptionResult:
    # Chargement du modèle (vous pouvez le mettre en cache global)
    model_name = "jonatasgrosman/wav2vec2-large-xlsr-53-french"
    processor = Wav2Vec2Processor.from_pretrained(model_name)
    model = Wav2Vec2ForCTC.from_pretrained(model_name)

    def sync_transcription():
        audio_input, sample_rate = sf.read(params.file_path)
        inputs = processor(audio_input, sampling_rate=16000, return_tensors="pt", padding=True)
        with torch.no_grad():
            logits = model(**inputs).logits
        predicted_ids = torch.argmax(logits, dim=-1)
        transcription = processor.batch_decode(predicted_ids)[0]
        return transcription.lower().strip()

    text = await asyncio.to_thread(sync_transcription)
    return TranscriptionResult(text=text)