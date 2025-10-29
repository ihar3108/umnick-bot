import os
from pydub import AudioSegment
import numpy as np

os.makedirs("audio", exist_ok=True)
rate = 44100
duration = 30
t = np.linspace(0, duration, int(rate * duration), False)

# Beatles – чистый тон 440 Гц (A4)
tone1 = np.sin(2 * np.pi * 440 * t) * 0.3
audio1 = (tone1 * 32767).astype(np.int16)
sound1 = AudioSegment(audio1.tobytes(), frame_rate=rate, sample_width=2, channels=1)
sound1.export("audio/beatles.mp3", format="mp3")

# Queen – тон 880 Гц (A5) + лёгкий tremolo
tone2 = np.sin(2 * np.pi * 880 * t) * 0.3 * (1 + 0.1 * np.sin(2 * np.pi * 4 * t))
audio2 = (tone2 * 32767).astype(np.int16)
sound2 = AudioSegment(audio2.tobytes(), frame_rate=rate, sample_width=2, channels=1)
sound2.export("audio/queen.mp3", format="mp3")

print("Создано 2 аудио-файла по 30 сек")
