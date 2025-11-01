import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from utils.dsp_functions import generate_signal, upsample_signal, downsample_signal

# Page title
st.title(" Signal Processing — Up/Down Sampling")
st.markdown("""
Explore how **upsampling** and **downsampling** affect digital signals.  
You can observe both **time-domain** and **frequency-domain** effects interactively.
""")

# Sidebar controls
st.sidebar.header("Sampling Parameters")
sig_type = st.sidebar.selectbox("Signal Type", ["Sine", "Cosine", "Square", "Sawtooth"])
amp = st.sidebar.slider("Amplitude", 0.1, 5.0, 1.0, 0.1)
freq = st.sidebar.slider("Frequency (Hz)", 1, 50, 5)
fs = st.sidebar.slider("Sampling Rate (Hz)", 50, 500, 100)
duration = st.sidebar.slider("Duration (s)", 0.5, 3.0, 1.0)
L = st.sidebar.slider("Upsampling Factor (L)", 1, 8, 2)
M = st.sidebar.slider("Downsampling Factor (M)", 1, 8, 2)

# Generate base signal
t, x = generate_signal(sig_type, amp, freq, 0, fs, duration)

# Apply upsampling & downsampling
x_up = upsample_signal(x, L)
x_down = downsample_signal(x, M)

# Time vectors after sampling
t_up = np.linspace(0, duration, len(x_up))
t_down = np.linspace(0, duration, len(x_down))

# Frequency analysis
def compute_fft(sig, fs):
    N = len(sig)
    X = np.fft.fft(sig)
    f = np.fft.fftfreq(N, 1/fs)
    return f[:N//2], np.abs(X[:N//2]) * 2 / N

f_orig, X_orig = compute_fft(x, fs)
f_up, X_up = compute_fft(x_up, fs * L)
f_down, X_down = compute_fft(x_down, fs / M)

# Plotting — time domain
st.subheader(" Time Domain Visualization")
fig_time, axs = plt.subplots(3, 1, figsize=(8, 6))
fig_time.subplots_adjust(hspace=0.5)

axs[0].plot(t, x, color='royalblue'); axs[0].set_title("Original Signal")
axs[1].stem(t_up[:150], x_up[:150], basefmt=" ", linefmt='darkorange', markerfmt='o')
axs[1].set_title(f"Upsampled Signal (×{L})")
axs[2].stem(t_down[:150], x_down[:150], basefmt=" ", linefmt='green', markerfmt='x')
axs[2].set_title(f"Downsampled Signal (÷{M})")

for ax in axs:
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Amplitude")
    ax.grid(alpha=0.3)

st.pyplot(fig_time)

# Plotting — frequency domain
st.subheader(" Frequency Domain (FFT Spectrum)")
fig_freq, axs2 = plt.subplots(3, 1, figsize=(8, 6))
fig_freq.subplots_adjust(hspace=0.5)

axs2[0].plot(f_orig, X_orig, color='royalblue'); axs2[0].set_title("Original Spectrum")
axs2[1].plot(f_up, X_up, color='darkorange'); axs2[1].set_title(f"Upsampled Spectrum (×{L})")
axs2[2].plot(f_down, X_down, color='green'); axs2[2].set_title(f"Downsampled Spectrum (÷{M})")

for ax in axs2:
    ax.set_xlabel("Frequency (Hz)")
    ax.set_ylabel("Magnitude")
    ax.grid(alpha=0.3)

st.pyplot(fig_freq)

# Info box
st.markdown("### ℹ Observations")
st.write(f"- Original sampling rate: **{fs} Hz**")
st.write(f"- After upsampling ×{L}: **{fs * L} Hz**")
st.write(f"- After downsampling ÷{M}: **{fs / M:.2f} Hz**")
st.info("Upsampling increases data rate (inserts zeros), while downsampling reduces it — potentially causing aliasing if not low-pass filtered.")
