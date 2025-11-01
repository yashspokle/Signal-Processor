import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from utils.dsp_functions import generate_signal, conv_signals

# --- Page Title ---
st.markdown(
    "<h2 style='text-align:center; color:#1E90FF;'> Convolution & Arithmetic Operations</h2>",
    unsafe_allow_html=True
)

st.write("Use the controls below to modify both signals before performing operations.")

# --- Signal Settings ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("Signal X[n]")
    sig1_type = st.selectbox("Type", ["Sine", "Cosine", "Square", "Sawtooth"])
    amp1 = st.slider("Amplitude", 0.1, 5.0, 1.0)
    freq1 = st.slider("Frequency (Hz)", 1, 20, 5)
    fs1 = st.slider("Sampling Rate (Hz)", 50, 500, 100)
    dur1 = st.slider("Duration (s)", 0.1, 2.0, 1.0)
    t1, x = generate_signal(sig1_type, amp=amp1, freq=freq1, fs=fs1, duration=dur1)

with col2:
    st.subheader("Signal H[n]")
    sig2_type = st.selectbox("Type ", ["Sine", "Cosine", "Square", "Sawtooth"])
    amp2 = st.slider("Amplitude ", 0.1, 5.0, 1.0)
    freq2 = st.slider("Frequency ", 1, 20, 3)
    fs2 = fs1  # Keep same sampling rate
    dur2 = dur1
    t2, h = generate_signal(sig2_type, amp=amp2, freq=freq2, fs=fs2, duration=dur2)

# --- Perform Operations ---
y_conv = conv_signals(x, h)
y_add = x[:len(h)] + h
y_mul = x[:len(h)] * h

# --- Plotting ---
st.markdown("### 📈 Visualization")

fig, axs = plt.subplots(4, 1, figsize=(10, 8))

axs[0].plot(t1, x, label="x[n]", color='royalblue')
axs[0].plot(t2, h, label="h[n]", color='orange', alpha=0.7)
axs[0].set_title("Input Signals")
axs[0].legend(); axs[0].grid(True)

axs[1].plot(y_conv, color='purple')
axs[1].set_title("Convolution Result y[n] = x[n] * h[n]")
axs[1].grid(True)

axs[2].plot(y_add, color='green')
axs[2].set_title("Addition: x[n] + h[n]")
axs[2].grid(True)

axs[3].plot(y_mul, color='red')
axs[3].set_title("Multiplication: x[n] × h[n]")
axs[3].grid(True)

fig.tight_layout()
st.pyplot(fig)

# --- Extra Info ---
st.markdown("---")
st.info("Tip: Adjust amplitude, frequency, or duration to see real-time changes in convolution and arithmetic results.")