import numpy as np
import librosa
import soundfile as sf
import io
from typing import Dict
from scipy import signal

class AudioService:
    def __init__(self):
        pass

    def process_audio(self, audio_data: bytes) -> bytes:
        # Load audio data
        audio_io = io.BytesIO(audio_data)
        y, sr = librosa.load(audio_io)
        
        # Apply noise reduction
        # 1. Median filtering to remove impulse noise
        y_clean = signal.medfilt(y)
        
        # 2. Apply spectral noise gate
        S = librosa.stft(y_clean)
        S_db = librosa.amplitude_to_db(np.abs(S))
        
        # Calculate noise threshold
        noise_threshold = np.median(S_db) + 1.5
        
        # Apply soft thresholding
        mask = librosa.db_to_amplitude(S_db - noise_threshold)
        mask = np.minimum(mask, 1)
        
        # Apply mask and reconstruct signal
        S_clean = S * mask
        y_clean = librosa.istft(S_clean)
        
        # Save processed audio to bytes
        output = io.BytesIO()
        sf.write(output, y_clean, sr, format='wav')
        return output.getvalue()

    def augment_audio(self, audio_data: bytes) -> bytes:
        # Load audio data
        audio_io = io.BytesIO(audio_data)
        y, sr = librosa.load(audio_io)
        
        # Apply pitch shift and time stretch
        y_shifted = librosa.effects.pitch_shift(y, sr=sr, n_steps=2)  # Shift pitch up by 2 semitones
        y_stretched = librosa.effects.time_stretch(y_shifted, rate=0.9)  # Slow down by 10%
        
        # Add reverb effect
        reverb = np.zeros_like(y_stretched)
        delay_samples = int(0.1 * sr)  # 100ms delay
        decay = 0.3
        for i in range(3):  # Add 3 echoes
            delay = delay_samples * (i + 1)
            if delay < len(reverb):
                reverb[delay:] += y_stretched[:-delay] * (decay ** (i + 1))
        
        y_augmented = y_stretched + 0.5 * reverb
        
        # Normalize
        y_augmented = y_augmented / np.max(np.abs(y_augmented))
        
        # Save augmented audio to bytes
        output = io.BytesIO()
        sf.write(output, y_augmented, sr, format='wav')
        return output.getvalue() 