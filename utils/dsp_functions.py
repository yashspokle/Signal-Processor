import numpy as np
from scipy.signal import convolve, resample, firwin, lfilter

def generate_signal(sig_type, amp=1, freq=5, phase=0, fs=100, duration=1):
    t = np.arange(0, duration, 1/fs)
    if sig_type == "Sine":
        x = amp * np.sin(2 * np.pi * freq * t + phase)
    elif sig_type == "Cosine":
        x = amp * np.cos(2 * np.pi * freq * t + phase)
    elif sig_type == "Square":
        x = amp * np.sign(np.sin(2 * np.pi * freq * t))
    elif sig_type == "Sawtooth":
        x = amp * 2*(t*freq - np.floor(t*freq + 0.5))
    elif sig_type == "Impulse":
        x = np.zeros_like(t); x[0] = amp
    else:
        x = np.random.randn(len(t))
    return t, x

def add_noise(x, noise_type="gaussian", level=0.1):
    if noise_type == "gaussian":
        return x + level * np.random.randn(len(x))
    elif noise_type == "impulse":
        p = 0.02
        mask = np.random.choice([0, 1], size=x.shape, p=[1-p, p])
        return x + mask * np.random.randn(*x.shape) * level
    return x

def remove_noise(x, fs, cutoff=10):
    b = firwin(51, cutoff/(fs/2))
    return lfilter(b, 1, x)

def conv_signals(x, h):
    return convolve(x, h, mode='full')

def upsample_signal(x, L):
    y = np.zeros(len(x)*L)
    y[::L] = x
    return y

def downsample_signal(x, M):
    return x[::M]
