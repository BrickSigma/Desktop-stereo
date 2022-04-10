"""
This module is responsible for recording the audio comming out of the main speakers
TO-DO: Implement a way to change current audio device automatically
"""

import sounddevice as sd

# Set the default device. To check all i/o devices, run print(sd.query_devices())
sd.default.device[0] = 2
fs = 44100
length = 1/9 # Length of recording in seconds

def record():
    recording = sd.rec(frames=int(fs*length), samplerate=fs, dtype="int16", blocking=True, channels=1)
    sd.wait()

    data = recording.flatten()

    return data