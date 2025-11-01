import streamlit as st

# Page setup
st.set_page_config(page_title="Signal Processing", page_icon="", layout="wide")

# Custom background + centered title
page_bg = """
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #1e3c72, #2a5298);
    color: white;
}
[data-testid="stHeader"] {background: rgba(0,0,0,0);}
h1, h2, h3, h4, h5, h6, p, div, span {
    color: #f0f0f0 !important;
}
.main-content {
    text-align: center;
    padding-top: 3rem;
}
.info-card {
    background-color: rgba(255, 255, 255, 0.08);
    padding: 1.5rem;
    border-radius: 15px;
    box-shadow: 0px 0px 10px rgba(255,255,255,0.1);
    transition: 0.3s ease;
}
.info-card:hover {
    transform: scale(1.02);
    background-color: rgba(255,255,255,0.12);
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# Title
st.markdown("<div class='main-content'>", unsafe_allow_html=True)
st.title(" Signal Processing")
st.subheader("Interactive Digital Signal Processing Web App")
st.markdown(
    """
Welcome to the **Signal Processing Application** — an interactive platform   
to help you **visualize and explore key DSP concepts** dynamically.

---

###  Features
<div class='info-card'>
<ul style='list-style-type:none; text-align:left;'>
<li> <b>Signal Generation</b> — Create and modify time-domain signals</li>
<li><b>Convolution & Arithmetic</b> — Combine and analyze signals</li>
<li> <b>Noise Filtering</b> — Add or remove different noise types</li>
<li> <b>Sampling Operations</b> — Upsample, Downsample, and reconstruct</li>
<li> <b>Aliasing </b> — Observe the effect of low sampling frequency</li>
</ul>
</div>

Use the <b>sidebar</b> to navigate through different DSP modules and experiment in real time.
    """,
    unsafe_allow_html=True
)

st.markdown("</div>", unsafe_allow_html=True)
