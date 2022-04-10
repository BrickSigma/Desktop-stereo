import sounddevice as sd
import numpy as np

sd.default.device[0] = 2
fs = 44100
length = 1/9 #s

def record():
    recording = sd.rec(frames=int(fs*length), samplerate=fs, dtype="int16", blocking=True, channels=1)
    sd.wait()

    data = recording.flatten()

    return data