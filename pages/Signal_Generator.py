import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from utils.dsp_functions import generate_signal

# Page title and intro
st.title(" Signal Processing — Signal Generator & Visualizer")
st.markdown("""
This interactive tool lets you **generate and visualize signals** in both 
time and frequency domains.  
Use the controls below to experiment with amplitude, frequency, and sampling rate!
""")

# Sidebar for controls
st.sidebar.header("Signal Parameters")
sig_type = st.sidebar.selectbox("Signal Type", ["Sine", "Cosine", "Square", "Sawtooth", "Impulse", "Random"])
amp = st.sidebar.slider("Amplitude", 0.1, 5.0, 1.0, 0.1)
freq = st.sidebar.slider("Frequency (Hz)", 1, 100, 5)
fs = st.sidebar.slider("Sampling Rate (Hz)", 50, 1000, 200)
duration = st.sidebar.slider("Duration (s)", 0.1, 5.0, 1.0)

# Generate signal
t, x = generate_signal(sig_type, amp, freq, 0, fs, duration)

# Compute FFT
N = len(x)
X_f = np.fft.fft(x)
freqs = np.fft.fftfreq(N, 1/fs)

# Plotting layout
fig, axs = plt.subplots(2, 1, figsize=(8, 6))
fig.subplots_adjust(hspace=0.5)

# Time domain plot
axs[0].plot(t, x, color='royalblue', linewidth=2)
axs[0].set_title(f"{sig_type} Signal in Time Domain", fontsize=12, fontweight='bold')
axs[0].set_xlabel("Time (s)")
axs[0].set_ylabel("Amplitude")
axs[0].grid(alpha=0.3)

# Frequency domain plot (magnitude spectrum)
axs[1].plot(freqs[:N//2], np.abs(X_f[:N//2]) * 2 / N, color='darkorange', linewidth=2)
axs[1].set_title("Frequency Spectrum", fontsize=12, fontweight='bold')
axs[1].set_xlabel("Frequency (Hz)")
axs[1].set_ylabel("Magnitude")
axs[1].grid(alpha=0.3)

# Display plots
st.pyplot(fig)

# Display key stats
st.markdown("###  Signal Information")
st.write(f"- **Signal Type:** {sig_type}")
st.write(f"- **Amplitude:** {amp}")
st.write(f"- **Frequency:** {freq} Hz")
st.write(f"- **Sampling Rate:** {fs} Hz")
st.write(f"- **Duration:** {duration} s")
st.write(f"- **Total Samples:** {N}")
