import numpy as np
import scipy.io.wavfile as wav
import os

# Create directories
if not os.path.exists("dataset/distress"):
    os.makedirs("dataset/distress")
if not os.path.exists("dataset/normal"):
    os.makedirs("dataset/normal")

SAMPLE_RATE = 16000
DURATION = 1 # seconds

def generate_sine_wave(freq, duration, sample_rate):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    # Generate sine wave
    wave = 0.5 * np.sin(2 * np.pi * freq * t)
    return wave

def generate_noise(duration, sample_rate):
    # White noise
    return np.random.uniform(-0.1, 0.1, int(sample_rate * duration))

print("Generating synthetic dataset...")

# Generate 50 'Scream' samples (High frequency sine waves + some noise)
for i in range(50):
    # Random high frequency between 800Hz and 2000Hz (Scream-like pitch)
    freq = np.random.randint(800, 2000)
    audio = generate_sine_wave(freq, DURATION, SAMPLE_RATE)
    # Add a little noise
    audio += np.random.uniform(-0.05, 0.05, len(audio))
    # Normalize
    audio = audio / np.max(np.abs(audio))
    wav.write(f"dataset/distress/scream_{i}.wav", SAMPLE_RATE, audio.astype(np.float32))

# Generate 50 'Normal' samples (White noise, low freq hum)
for i in range(50):
    # Low frequency hum or just noise
    if i % 2 == 0:
        audio = generate_noise(DURATION, SAMPLE_RATE)
    else:
        freq = np.random.randint(50, 300) # Normal speech/hum range
        audio = generate_sine_wave(freq, DURATION, SAMPLE_RATE) * 0.3
        
    wav.write(f"dataset/normal/noise_{i}.wav", SAMPLE_RATE, audio.astype(np.float32))

print("Done! Generated 100 synthetic files in 'dataset/' folders.")
print("Now run 'python train_model.py' to train the model.")
