[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.32%2B-red.svg)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
A high-performance, real-time audio processing and pitch-detection application engineered to analyze live acoustic piano performance. Built with **Streamlit**, **NumPy**, and **sounddevice**, this tool maps raw microphone input to musical pitch classes and octaves with low latency, providing immediate visual feedback for aspiring musicians.
cat << 'EOF' > README.md
# 🎹 Piano Live Tutor

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.32%2B-red.svg)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A high-performance, real-time audio processing and pitch-detection application engineered to analyze live acoustic piano performance. Built with **Streamlit**, **NumPy**, and **sounddevice**, this tool maps raw microphone input to musical pitch classes and octaves with low latency, providing immediate visual feedback for aspiring musicians.

---
* **Frontend & Dashboard:** `Streamlit` for reactive, stateful browser rendering and UI control loops.
* **Audio Capture:** `sounddevice` configured with non-blocking callback streams to handle continuous PCM audio frames safely without dropping buffers.
* **DSP & Pitch Extraction:** `NumPy` executing Fast Fourier Transforms (FFT), window functions to mitigate spectral leakage, and peak detection algorithms to isolate fundamental frequencies ($f_0$).

---

## ⚙️ Core Algorithmic Workflow

1. **Buffer Acquisition:** Audio is streamed in real-time blocks (PCM chunks) from the system's default input device at a controlled sample rate ($44.1\,\text{kHz}$).
2. **Spectral Windowing:** A Hann window is applied to each audio frame to reduce spectral leakage and boundary discontinuities before transformation.
3. **Frequency Bin Mapping:** The discrete frequency spectrum is computed using vectorized NumPy FFT operations, mapping energy spikes to standard musical scale semitones ($A_4 = 440\,\text{Hz}$).
4. **Note & Octave Resolution:** Frequencies are translated into scientific pitch notation via logarithmic frequency scaling:
   $$n = 12 \times \log_2\left(\frac{f}{440}\right) + 69$$

---

## 🚀 Quickstart & Local Installation

Clone the repository and install dependencies locally:

```bash
# Clone the repository
git clone [https://github.com/estiaarexy/piano-live-tutor.git](https://github.com/estiaarexy/piano-live-tutor.git)
cd piano-live-tutor

# Install required audio and UI dependencies
pip install streamlit sounddevice numpy

# Run the application locally
streamlit run app.py
