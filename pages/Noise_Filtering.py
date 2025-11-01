import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from utils.dsp_functions import generate_signal, add_noise, remove_noise
from scipy.signal import firwin, lfilter, freqz

# --- Page Setup ---
st.markdown(
    "<h2 style='text-align:center; color:#1E90FF;'> Noise Addition & Filtering</h2>",
    unsafe_allow_html=True
)

st.write("Use this module to add noise to a signal and apply different filters interactively.")

# --- Signal Settings ---
st.sidebar.header("🎛 Signal Controls")
sig_type = st.sidebar.selectbox("Signal Type", ["Sine", "Cosine", "Square", "Sawtooth"])
amp = st.sidebar.slider("Amplitude", 0.1, 5.0, 1.0)
freq = st.sidebar.slider("Frequency (Hz)", 1, 50, 5)
fs = st.sidebar.slider("Sampling Rate (Hz)", 50, 500, 100)
duration = st.sidebar.slider("Duration (s)", 0.1, 3.0, 1.0)

t, x = generate_signal(sig_type, amp=amp, freq=freq, fs=fs, duration=duration)

# --- Noise Controls ---
st.sidebar.header(" Noise Controls")
noise_type = st.sidebar.selectbox("Noise Type", ["Gaussian", "Uniform", "Impulse"])
noise_level = st.sidebar.slider("Noise Level", 0.0, 1.0, 0.2)

# Add noise
x_noisy = add_noise(x, noise_type.lower(), noise_level)

# --- Filter Settings ---
st.sidebar.header("🎚 Filter Controls")
filter_type = st.sidebar.selectbox("Filter Type", ["Low-pass", "High-pass", "Band-pass"])
cutoff_low = st.sidebar.slider("Low Cutoff (Hz)", 1, int(fs//4), 5)
cutoff_high = st.sidebar.slider("High Cutoff (Hz)", cutoff_low+1, int(fs//2), 20)

# --- Apply Filter ---
if filter_type == "Low-pass":
    b = firwin(101, cutoff_low / (fs/2), pass_zero=True)
elif filter_type == "High-pass":
    b = firwin(101, cutoff_low / (fs/2), pass_zero=False)
else:  # Band-pass
    b = firwin(101, [cutoff_low / (fs/2), cutoff_high / (fs/2)], pass_zero=False)

x_clean = lfilter(b, 1, x_noisy)

# --- Frequency Spectrum Helper ---
def get_spectrum(signal, fs):
    n = len(signal)
    freq_axis = np.fft.rfftfreq(n, d=1/fs)
    spectrum = np.abs(np.fft.rfft(signal)) / n
    return freq_axis, spectrum

# --- Plotting Section ---
st.markdown("###  Time Domain Comparison")

fig1, axs = plt.subplots(3, 1, figsize=(10, 8))
axs[0].plot(t, x, label="Original", color='royalblue')
axs[1].plot(t, x_noisy, label="Noisy", color='darkorange')
axs[2].plot(t, x_clean, label="Filtered", color='green')
for ax in axs:
    ax.legend()
    ax.grid(True)
axs[0].set_title("Original Signal")
axs[1].set_title(f"{noise_type} Noise Added")
axs[2].set_title(f"{filter_type} Filter Output")
fig1.tight_layout()
st.pyplot(fig1)

# --- Frequency Domain Comparison ---
st.markdown("### ⚡ Frequency Domain Comparison")

f_x, X = get_spectrum(x, fs)
f_n, Xn = get_spectrum(x_noisy, fs)
f_f, Xf = get_spectrum(x_clean, fs)

fig2, ax2 = plt.subplots(figsize=(10,4))
ax2.plot(f_x, X, label="Original", color='royalblue')
ax2.plot(f_n, Xn, label="Noisy", color='darkorange', alpha=0.6)
ax2.plot(f_f, Xf, label="Filtered", color='green')
ax2.set_xlabel("Frequency (Hz)")
ax2.set_ylabel("Magnitude")
ax2.set_title("Frequency Response Comparison")
ax2.legend()
ax2.grid(True)
st.pyplot(fig2)

# --- Filter Frequency Response ---
st.markdown("###  Filter Response")
w, h = freqz(b, worN=8000)
fig3, ax3 = plt.subplots(figsize=(10,3))
ax3.plot((fs * 0.5 / np.pi) * w, 20 * np.log10(abs(h)), color='purple')
ax3.set_title("Filter Magnitude Response")
ax3.set_xlabel("Frequency (Hz)")
ax3.set_ylabel("Gain (dB)")
ax3.grid(True)
st.pyplot(fig3)

# --- Info ---
st.markdown("---")
st.info(
    " **Tip:** Try increasing the noise level or switching between filter types to see how each affects signal clarity and spectral content."
)
