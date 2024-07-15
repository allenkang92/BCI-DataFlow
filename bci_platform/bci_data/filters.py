import numpy as np
from scipy import signal

def bandpass_filter(data, lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = signal.butter(order, [low, high], btype='band')
    return signal.filtfilt(b, a, data)

def notch_filter(data, notch_freq, fs, q=30):
    w0 = notch_freq / (fs/2)
    b, a = signal.iirnotch(w0, q)
    return signal.filtfilt(b, a, data)