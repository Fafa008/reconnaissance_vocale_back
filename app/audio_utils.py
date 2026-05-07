import librosa
import soundfile as sf
import numpy as np

def load_and_normalize(audio_array, sr):
    # Resample
    if sr != 16000:
        audio_array = librosa.resample(audio_array, sr, 16000)

    # Normalize amplitude
    audio_array = audio_array / np.max(np.abs(audio_array) + 1e-9)

    return audio_array, 16000

def save_audio(path, audio, sr=16000):
    sf.write(path, audio, sr)