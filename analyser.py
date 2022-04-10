"""
This module is used for analysing the audio from the speakers.
TO-DO: Apply noise reduction to the audio for smoother result.
"""

from scipy.fftpack import rfft, rfftfreq
import numpy as np
from numba import jit

# numba.jit speed up to prevent the analyser from lagging
@jit(nopython = True, cache = True, fastmath = True)
def loop(xf, yf, amps):

    max = float(yf.max())
    lim = float(yf.max()/4)

    res = np.where(np.logical_and(xf >= 0, xf <= 60))
    y = np.copy(yf[res])
    res = np.where(y >= lim)
    if len(y) == 0:
        amps = np.append(amps, 0)
    else:
        amps = np.append(amps, y.mean()/max)

    res = np.where(np.logical_and(xf > 60, xf <= 150))
    y = np.copy(yf[res])
    res = np.where(y >= lim)
    y = np.copy(y[res])
    if len(y) == 0:
        amps = np.append(amps, 0)
    else:
        amps = np.append(amps, y.mean()/max)

    res = np.where(np.logical_and(xf > 150, xf <= 400))
    y = np.copy(yf[res])
    res = np.where(y >= lim)
    y = np.copy(y[res])
    if len(y) == 0:
        amps = np.append(amps, 0)
    else:
        amps = np.append(amps, y.mean()/max)

    res = np.where(np.logical_and(xf > 400, xf <= 1000))
    y = np.copy(yf[res])
    res = np.where(y >= lim)
    y = np.copy(y[res])
    if len(y) == 0:
        amps = np.append(amps, 0)
    else:
        amps = np.append(amps, y.mean()/max)

    res = np.where(np.logical_and(xf > 1000, xf <= 2400))
    y = np.copy(yf[res])
    res = np.where(y >= lim)
    y = np.copy(y[res])
    if len(y) == 0:
        amps = np.append(amps, 0)
    else:
        amps = np.append(amps, y.mean()/max)

    res = np.where(np.logical_and(xf > 2400, xf <= 6000))
    y = np.copy(yf[res])
    res = np.where(y >= lim)
    y = np.copy(y[res])
    if len(y) == 0:
        amps = np.append(amps, 0)
    else:
        amps = np.append(amps, y.mean()/max)

    res = np.where(xf > 6000)
    y = np.copy(yf[res])
    res = np.where(y >= lim)
    y = np.copy(y[res])
    if len(y) == 0:
        amps = np.append(amps, 0)
    else:
        amps = np.append(amps, y.mean()/max)

    return amps

def analyse(data):
    """
    Analyse the audio data and split it into frequency ranges using FFT
    Parameters:
        data: numpy.ndarray containing audio data
    """
    N = int(data.size)

    yf = np.array(np.abs(rfft(data)), np.float64)
    xf = rfftfreq(N, 1 / 44100)

    if np.std(yf) <= 100:
        amps = np.array([0, 0, 0, 0, 0, 0, 0], np.float64)
    else:
        amps = np.array([], np.float64)
        amps = loop(xf, yf, amps)

    return amps