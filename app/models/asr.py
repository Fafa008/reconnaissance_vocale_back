import torch
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
from app.config import MODEL_NAME, USE_GPU

class ASRModel:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load_model()
        return cls._instance

    def _load_model(self):
        print(f"Chargement du modèle {MODEL_NAME}...")
        self.processor = Wav2Vec2Processor.from_pretrained(MODEL_NAME)
        self.model = Wav2Vec2ForCTC.from_pretrained(MODEL_NAME)
        if USE_GPU and torch.cuda.is_available():
            self.model = self.model.cuda()
        self.model.eval()
        print("Modèle prêt.")

    def transcribe(self, audio_array):
        inputs = self.processor(audio_array, sampling_rate=16000, return_tensors="pt")
        if USE_GPU and torch.cuda.is_available():
            inputs = {k: v.cuda() for k, v in inputs.items()}
        with torch.no_grad():
            logits = self.model(**inputs).logits
        predicted_ids = torch.argmax(logits, dim=-1)
        return self.processor.batch_decode(predicted_ids)[0].lower().strip()

asr_model = ASRModel()