# Piano Live Tutor

A practice tool that listens to your piano through the microphone and checks
whether you play the right notes, from a single note up to the opening of
Für Elise.

## How it works
1. Records a short audio window for each note (2.0 s; 1.1 s for Für Elise)
2. Takes the FFT of the recording and finds the strongest frequency
3. Matches that frequency to the nearest note in a piano frequency table (A3-A5)
4. Compares it with the target note in the practice sequence

## Features
- 9 levels, from a single note (C4) to the opening of Für Elise
- Level selector with step-by-step feedback
- Restart and home controls

## Run locally
    git clone https://github.com/estiaarexy/piano-live-tutor
    cd piano-live-tutor
    pip install -r requirements.txt
    streamlit run app.py

A working microphone is required. Allow microphone access when prompted.

## Current limitations
- Needs a local microphone, so the hosted demo cannot listen to visitors
- Fixed-length recordings, not continuous detection
- Single notes only; no chords
- No silence or noise handling yet
- Accuracy not yet measured across all notes

## Planned
- Silence detection and a rewritten pitch detector
- Accuracy results per note
- Browser microphone support
- Practice history and scoring
  

