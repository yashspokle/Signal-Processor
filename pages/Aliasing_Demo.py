import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# ---- Page Title ----
st.title(" Aliasing")
st.markdown("""
Understand how **sampling frequency** affects the captured signal.  
When sampling below the **Nyquist rate (2×signal frequency)**, aliasing occurs — the signal appears distorted or “flipped” in frequency.
""")

# ---- Controls ----
freq_signal = st.slider(" Signal Frequency (Hz)", 1, 100, 10)
fs = st.slider(" Sampling Frequency (Hz)", 10, 200, 50)
duration = st.slider("Signal Duration (s)", 0.5, 2.0, 1.0)

# ---- Generate signals ----
t_cont = np.linspace(0, duration, 1000)  # continuous reference
x_cont = np.sin(2 * np.pi * freq_signal * t_cont)

t_samp = np.arange(0, duration, 1/fs)
x_samp = np.sin(2 * np.pi * freq_signal * t_samp)

# ---- Time Domain Plot ----
st.subheader(" Time Domain Visualization")
fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(t_cont, x_cont, 'b', alpha=0.6, label="Continuous Signal")
ax.stem(t_samp, x_samp, basefmt=" ", linefmt='r', markerfmt='ro', label="Sampled Points")
ax.set_title(f"Aliasing Visualization — Signal: {freq_signal} Hz | Sampling: {fs} Hz")
ax.set_xlabel("Time (s)")
ax.set_ylabel("Amplitude")
ax.legend()
ax.grid(alpha=0.3)
st.pyplot(fig)

# ---- Frequency Spectrum ----
st.subheader(" Frequency Domain (Magnitude Spectrum)")

N = len(x_samp)
X = np.fft.fft(x_samp)
freqs = np.fft.fftfreq(N, 1/fs)
mag = np.abs(X)[:N//2] * 2 / N

fig2, ax2 = plt.subplots(figsize=(8, 4))
ax2.plot(freqs[:N//2], mag, 'g')
ax2.set_title("Spectrum of Sampled Signal")
ax2.set_xlabel("Frequency (Hz)")
ax2.set_ylabel("Magnitude")
ax2.grid(alpha=0.3)
st.pyplot(fig2)

# ---- Interpretation ----
st.markdown("###  Interpretation:")
nyquist = fs / 2
if fs < 2 * freq_signal:
    st.error(f" **Aliasing Occurs!** Sampling rate ({fs} Hz) < Nyquist rate ({2*freq_signal} Hz)")
else:
    st.success(f" No aliasing. Sampling rate ({fs} Hz) ≥ Nyquist rate ({2*freq_signal} Hz)")

st.info("Try lowering the sampling frequency below twice the signal frequency to observe aliasing visually and in the spectrum.")
