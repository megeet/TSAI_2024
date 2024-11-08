import numpy as np
import librosa
import soundfile as sf
import io
from typing import Dict, Tuple
from scipy import signal
import base64
import matplotlib.pyplot as plt

class AudioService:
    def __init__(self):
        pass

    def process_audio(self, audio_data: bytes) -> Dict[str, bytes]:
        # Load audio data
        audio_io = io.BytesIO(audio_data)
        y, sr = librosa.load(audio_io)
        
        # 1. Process audio (multiple techniques)
        # a. Frequency increase
        new_sr = int(sr * 2.0)  # 100% increase
        y_freq = librosa.resample(y, orig_sr=sr, target_sr=new_sr)
        
        # b. Apply bandpass filter (keep only mid-range frequencies)
        nyquist = sr / 2
        low_cutoff = 500 / nyquist
        high_cutoff = 4000 / nyquist
        b, a = signal.butter(4, [low_cutoff, high_cutoff], btype='band')
        y_filtered = signal.filtfilt(b, a, y)
        
        # c. Apply compression (reduce dynamic range)
        threshold = 0.1
        ratio = 4.0
        y_compressed = np.zeros_like(y)
        for i, sample in enumerate(y):
            if abs(sample) > threshold:
                if sample > 0:
                    y_compressed[i] = threshold + (sample - threshold) / ratio
                else:
                    y_compressed[i] = -threshold + (sample + threshold) / ratio
            else:
                y_compressed[i] = sample
        
        # Combine all processed versions
        y_processed = (y_freq[:len(y)] + y_filtered + y_compressed) / 3
        
        # Normalize
        y_processed = y_processed / np.max(np.abs(y_processed))
        
        # Save processed audio to bytes
        audio_output = io.BytesIO()
        sf.write(audio_output, y_processed, new_sr, format='wav')
        
        # 2. Compute and visualize MFCC
        mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        
        # Create MFCC visualization
        plt.figure(figsize=(10, 4))
        librosa.display.specshow(mfccs, x_axis='time', sr=sr)
        plt.colorbar(format='%+2.0f dB')
        plt.title('MFCC')
        plt.tight_layout()
        
        # Save plot to bytes
        mfcc_output = io.BytesIO()
        plt.savefig(mfcc_output, format='png')
        plt.close()
        
        return {
            "processed_audio": audio_output.getvalue(),
            "mfcc_plot": mfcc_output.getvalue()
        }

    def augment_audio(self, audio_data: bytes) -> bytes:
        # Load original audio data
        audio_io = io.BytesIO(audio_data)
        y, sr = librosa.load(audio_io)
        
        # 1. Apply pitch shift and time stretch
        y_shifted = librosa.effects.pitch_shift(y, sr=sr, n_steps=2)
        y_stretched = librosa.effects.time_stretch(y_shifted, rate=0.9)
        
        # 2. Add harmonic enhancement
        y_harmonic = librosa.effects.harmonic(y_stretched)
        
        # 3. Add chorus effect
        chorus = np.zeros_like(y_harmonic)
        num_voices = 3
        for i in range(num_voices):
            delay = int(sr * (0.02 + 0.01 * i))  # Different delay for each voice
            rate = 0.5 + 0.1 * i  # Different rate for each voice
            depth = 0.002  # Modulation depth
            t = np.arange(len(y_harmonic)) / sr
            mod = depth * np.sin(2 * np.pi * rate * t)
            delay_samples = (delay + (mod * sr).astype(int)) % len(y_harmonic)
            chorus += y_harmonic[delay_samples] * (0.5 ** (i + 1))
        
        # Combine original and chorus
        y_augmented = y_harmonic + 0.5 * chorus
        
        # 4. Add reverb
        reverb = np.zeros_like(y_augmented)
        delay_samples = int(0.1 * sr)
        decay = 0.3
        for i in range(3):
            delay = delay_samples * (i + 1)
            if delay < len(reverb):
                reverb[delay:] += y_augmented[:-delay] * (decay ** (i + 1))
        
        y_augmented = y_augmented + 0.3 * reverb
        
        # Normalize
        y_augmented = y_augmented / np.max(np.abs(y_augmented))
        
        # Save augmented audio to bytes
        output = io.BytesIO()
        sf.write(output, y_augmented, sr, format='wav')
        return output.getvalue()