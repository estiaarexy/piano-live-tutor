import streamlit as st
import numpy as np
import sounddevice as sd
import time

# Page configuration
st.set_page_config(page_title="🎹 Real-Time Audio Piano Trainer", layout="centered")

# --- CUSTOM CSS STYLING ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #1e1e2f 0%, #2a2a40 100%);
        color: #ffffff;
    }
    .title-banner {
        background: linear-gradient(90deg, #6a11cb 0%, #2575fc 100%);
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        color: white;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        margin-bottom: 20px;
    }
    .target-box {
        padding: 35px;
        border-radius: 15px;
        background: rgba(255, 255, 255, 0.05);
        text-align: center;
        border: 3px solid #00d2ff;
        box-shadow: 0 0 25px rgba(0, 210, 255, 0.3);
        margin-bottom: 20px;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #00c6ff 0%, #0072ff 100%);
        color: white;
        font-weight: bold;
        border: none;
        padding: 14px;
        border-radius: 8px;
        font-size: 16px;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #0072ff 0%, #00c6ff 100%);
        box-shadow: 0 0 15px rgba(0, 198, 255, 0.5);
    }
    </style>
""", unsafe_allow_html=True)

# State management
if "page" not in st.session_state:
    st.session_state.page = "home"
if "level" not in st.session_state:
    st.session_state.level = 0

# Sequences mapped with precise octaves (C4/D4 for scales, E5/D#5/B4 for Für Elise)
sequences = {
    0: ["C4"],
    1: ["C4", "D4"],
    2: ["C4", "D4", "E4"],
    3: ["C4", "E4", "D4"],
    4: ["C4", "D4", "E4", "F4"],
    5: ["C4", "F4", "E4", "D4"],
    6: ["C4", "D4", "E4", "F4", "G4"],
    7: ["C4", "D4", "E4", "F4", "G4", "A4", "B4"],
    8: [  # Für Elise Opening Theme in correct higher octaves
        "E5", "D#5", "E5", "D#5", "E5", "B4", "D5", "C5", "A4",
        "C4", "E4", "A4", "B4",
        "E4", "G#4", "B4", "C5",
        "E5", "D#5", "E5", "D#5", "E5", "B4", "D5", "C5", "A4",
        "C4", "E4", "A4", "B4",
        "E4", "C5", "B4", "A4"
    ]
}

level_names = {
    0: "Level 1: Single Note (C4)",
    1: "Level 2: Two Notes (C4 → D4)",
    2: "Level 3: Tri-Note Scale (C4 → D4 → E4)",
    3: "Level 4: Alternate Pattern (C4 → E4 → D4)",
    4: "Level 5: Four Notes (C4 → D4 → E4 → F4)",
    5: "Level 6: Melodic Jump (C4 → F4 → E4 → D4)",
    6: "Level 7: Five Notes (C4 → D4 → E4 → F4 → G4)",
    7: "Level 8: Full Octave Scale (C4 to B4)",
    8: "Level 9: 🎵 Für Elise Full Theme (Octave-Correct)"
}

# Scientific Pitch Frequencies (Hz)
NOTE_FREQUENCIES = {
    "A3": 220.00,
    "B3": 246.94,
    "C4": 261.63,
    "C#4": 277.18,
    "D4": 293.66,
    "D#4": 311.13,
    "E4": 329.63,
    "F4": 349.23,
    "F#4": 369.99,
    "G4": 392.00,
    "G#4": 415.30,
    "A4": 440.00,
    "A#4": 466.16,
    "B4": 493.88,
    "C5": 523.25,
    "C#5": 554.37,
    "D5": 587.33,
    "D#5": 622.25,
    "E5": 659.25,
    "F5": 698.46,
    "G5": 783.99,
    "A5": 880.00
}

def frequency_to_note(frequency):
    if frequency < 50:
        return None
    closest_note = min(NOTE_FREQUENCIES.keys(), key=lambda n: abs(NOTE_FREQUENCIES[n] - frequency))
    if abs(NOTE_FREQUENCIES[closest_note] - frequency) < 22:
        return closest_note
    return None

def listen_for_note(duration_seconds):
    fs = 44100
    audio_data = sd.rec(int(duration_seconds * fs), samplerate=fs, channels=1, dtype='float32')
    audio_data = np.ascontiguousarray(audio_data)
    sd.wait()
    
    audio_data = audio_data.flatten()
    fft_spectrum = np.fft.rfft(audio_data)
    freqs = np.fft.rfftfreq(len(audio_data), 1/fs)
    
    peak_freq = freqs[np.argmax(np.abs(fft_spectrum))]
    return frequency_to_note(peak_freq)

# --- HOME PAGE ---
if st.session_state.page == "home":
    st.markdown("""
        <div class="title-banner">
            <h1>🎹 Real-Time Interactive Piano Trainer</h1>
            <p style="font-size: 18px; margin: 0;">Octave-Accurate Paced Practice Studio</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(
        """
        <div style="text-align: center; padding: 25px; background: rgba(255,255,255,0.03); border-radius: 10px; border: 1px solid #444;">
            <h2 style="color: #00c6ff;">⏱️ 🎹 🎶</h2>
            <p style="font-size: 16px; color: #ddd;">
               Jump straight to any scale or song. Scientific pitch mapping ensures every octave (C4, B4, E5) is spot on!
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.write("")
    if st.button("🚀 Launch Training Studio", use_container_width=True):
        st.session_state.page = "app"
        st.rerun()

# --- APP PRACTICE PAGE ---
elif st.session_state.page == "app":
    st.markdown("""
        <div class="title-banner" style="padding: 15px;">
            <h2>🎵 Automated Paced Practice Mode</h2>
        </div>
    """, unsafe_allow_html=True)
    
    # LEVEL SELECTOR DROPDOWN
    selected_level_name = st.selectbox(
        "📂 Select Practice Level or Song:",
        options=list(level_names.values()),
        index=st.session_state.level
    )
    
    for lvl_id, name in level_names.items():
        if name == selected_level_name:
            st.session_state.level = lvl_id
            break

    current_seq = sequences[st.session_state.level]
    
    st.markdown(f"### 📍 Target Sequence: `{' → '.join(current_seq[:10])}{'...' if len(current_seq) > 10 else ''}`")
    
    display_container = st.empty()
    feedback_container = st.empty()
    
    display_container.markdown(
        f"""
        <div class="target-box">
            <h4 style="color: #00d2ff; margin: 0; text-transform: uppercase;">Ready for {selected_level_name}?</h4>
            <h1 style="font-size: 40px; margin: 15px 0; color: #ffffff;">🎹 Press Start Below</h1>
            <p style="margin: 0; color: #bbb;">Octave-precise rhythm pacing enabled.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    if st.button(f"▶️ Start Automated Sequence", use_container_width=True):
        success_all = True
        
        # 1.1s window for Für Elise (Level 8), 2.0s for scales
        note_duration = 1.1 if st.session_state.level == 8 else 2.0
        
        for idx, target_note in enumerate(current_seq):
            display_container.markdown(
                f"""
                <div class="target-box" style="border-color: #ff007f; box-shadow: 0 0 25px rgba(255,0,127,0.4);">
                    <h4 style="color: #ff007f; margin: 0;">NOW PLAYING (Note {idx+1} of {len(current_seq)}):</h4>
                    <h1 style="font-size: 85px; margin: 15px 0; color: #ffffff; text-shadow: 0 0 20px rgba(255,0,127,0.6);">🎹 {target_note}</h1>
                    <p style="margin: 0; color: #ff88cc;">Listening ({note_duration}s window)... Play it now!</p>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            detected_note = listen_for_note(note_duration)
            
            if detected_note == target_note:
                feedback_container.success(f"✅ Step {idx+1}: Played **{target_note}** correctly!")
            else:
                feedback_container.error(f"❌ Step {idx+1}: Expected **{target_note}**, but heard **{detected_note}**. Sequence failed!")
                success_all = False
                break
                
            time.sleep(0.15)
            
        if success_all:
            st.balloons()
            st.success(f"🎉 AMAZING! You successfully completed `{selected_level_name}`!")
            if st.session_state.level < len(sequences) - 1:
                st.session_state.level += 1
            time.sleep(2.0)
            st.rerun()
        else:
            st.warning("⚠️ Practice round interrupted. Hit start to try again!")

    st.write("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Restart Level"):
            st.rerun()
    with col2:
        if st.button("🏠 Back to Home"):
            st.session_state.page = "home"
            st.session_state.level = 0
            st.rerun()