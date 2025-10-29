import os, wave, struct, math

os.makedirs("audio", exist_ok=True)

rate = 44100
duration = 30
frames = int(rate * duration)

# Beatles – 440 Гц (A4)
with wave.open("audio/beatles.wav", "w") as w:
    w.setnchannels(1)
    w.setsampwidth(2)
    w.setframerate(rate)
    for i in range(frames):
        value = int(32767 * 0.3 * math.sin(2 * math.pi * 440 * i / rate))
        w.writeframes(struct.pack('<h', value))

# Queen – 880 Гц (A5) + tremolo
with wave.open("audio/queen.wav", "w") as w:
    w.setnchannels(1)
    w.setsampwidth(2)
    w.setframerate(rate)
    for i in range(frames):
        tremolo = 1 + 0.1 * math.sin(2 * math.pi * 4 * i / rate)
        value = int(32767 * 0.3 * tremolo * math.sin(2 * math.pi * 880 * i / rate))
        w.writeframes(struct.pack('<h', value))

print("Создано 2 WAV-файла по 30 сек")
