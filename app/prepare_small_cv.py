import os
import librosa
import soundfile as sf
import numpy as np
from datasets import load_dataset
from tqdm import tqdm

OUTPUT_DIR = "data/small_cv/train"
SAMPLE_RATE = 16000
MAX_SAMPLES = 100  # Télécharge seulement 100 fichiers pour un test rapide

os.makedirs(OUTPUT_DIR, exist_ok=True)

def load_and_normalize(audio_array, orig_sr):
    if orig_sr != SAMPLE_RATE:
        audio_array = librosa.resample(audio_array, orig_sr=orig_sr, target_sr=SAMPLE_RATE)
    max_val = np.max(np.abs(audio_array))
    if max_val > 0:
        audio_array = audio_array / max_val
    return audio_array, SAMPLE_RATE

def save_audio(path, audio, sr=SAMPLE_RATE):
    sf.write(path, audio, sr)

print("Chargement du dataset Common Voice 17.0 en streaming...")
dataset = load_dataset("fsicoli/common_voice_17_0", "fr", split="train", streaming=True)

print(f"Extraction des {MAX_SAMPLES} premiers échantillons...")
for i, sample in enumerate(tqdm(dataset, total=MAX_SAMPLES)):
    if i >= MAX_SAMPLES:
        break

    # Récupération des données
    audio = sample["audio"]["array"]
    sr = sample["audio"]["sampling_rate"]
    text = sample["sentence"].strip().lower()

    audio_norm, _ = load_and_normalize(audio, sr)

    wav_path = os.path.join(OUTPUT_DIR, f"cv_{i:04d}.wav")
    txt_path = os.path.join(OUTPUT_DIR, f"cv_{i:04d}.txt")

    save_audio(wav_path, audio_norm)
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(text)

print(f"Terminé. {MAX_SAMPLES} fichiers sauvegardés dans {OUTPUT_DIR}")