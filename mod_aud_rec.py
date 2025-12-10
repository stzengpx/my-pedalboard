import os
import numpy as np
import soundfile as sf
from datetime import datetime

class AudioRecorder:
    def __init__(self, sample_rate):
        self.sample_rate = sample_rate
        self.frames = []
        self.is_recording = False

    def start(self):
        self.is_recording = True
        self.frames = []
        print("🔴 Recording started...")

    def add_frame(self, data):
        if self.is_recording:
            # Make a copy to avoid threading issues
            self.frames.append(data.copy())

    def save(self, output_dir="output", timestamp=None, suffix=""):
        if not self.frames:
            print(f"⚠️ No audio recorded for {suffix}.")
            return

        # Ensure directory exists
        os.makedirs(output_dir, exist_ok=True)

        # Create filename: DateYYYYMMDDhhmmss.xxx-suffix.mp3
        if timestamp is None:
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S.%f")[:18] #.xxx for millis
        
        filename = f"rec-{timestamp}{suffix}.mp3"
        filepath = os.path.join(output_dir, filename)

        print(f"💾 Saving recording to {filepath}...")
        
        try:
            # Concatenate all frames
            audio_data = np.concatenate(self.frames, axis=0)
            
            # Save using soundfile
            # Note: writing to MP3 requires libmp3lame. 
            # If it fails, soundfile usually raises an error.
            sf.write(filepath, audio_data, self.sample_rate)
            print("✅ Save complete.")
        except Exception as e:
            print(f"❌ Error saving file: {e}")
            # Fallback to WAV if MP3 fails
            try:
                wav_path = filepath.replace(".mp3", ".wav")
                print(f"🔄 Retrying as WAV: {wav_path}")
                sf.write(wav_path, audio_data, self.sample_rate)
                print("✅ Saved as WAV.")
            except Exception as e2:
                print(f"❌ WAV fallback failed: {e2}")
