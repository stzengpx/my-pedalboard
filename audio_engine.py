import sounddevice as sd
import numpy as np
from datetime import datetime
import audio_config
import fx_custom 

# We import these for type checking compatibility if needed, 
# but mostly we just iterate the chain.

class PedalboardEngine:
    """
    Manages the realtime audio stream, effect processing loop, and recording.
    """
    def __init__(self, clean_recorder=None, fx_recorder=None, plugin_chain=None):
        self.clean_recorder = clean_recorder
        self.fx_recorder = fx_recorder
        self.chain = plugin_chain if plugin_chain else []
        
    def _audio_callback(self, indata, outdata, frames, time, status):
        """
        Realtime audio callback called by sounddevice.
        """
        if status:
            print(f"⚠️ Audio Status: {status}")
        
        # 1. Record Clean Input
        if self.clean_recorder:
            self.clean_recorder.add_frame(indata)

        # 2. Process Audio Chain
        # We start with the input signal
        current_signal = indata
        
        try:
            for effect in self.chain:
                # Efficient logic to determine how to call the effect
                if hasattr(effect, '__class__') and effect.__class__.__module__ == 'fx_custom':
                     # Custom Python effects expect (samples, channels)
                    current_signal = effect(current_signal, audio_config.SAMPLE_RATE)
                else:
                    # Standard Pedalboard (C++) effects expect (channels, samples)
                    # We transpose before and after
                    current_signal = effect(current_signal.T, sample_rate=audio_config.SAMPLE_RATE).T
                    
        except Exception as e:
            # Failsafe: If DSP crashes, we don't want to crash the thread if possible,
            # or allow it to pass through dry signal.
            # Printing ensures we see the error.
            print(f"❌ DSP Error: {e}")
        
        # 3. Write processed audio to output
        outdata[:] = current_signal

        # 4. Record FX Output
        if self.fx_recorder:
            self.fx_recorder.add_frame(outdata)

    def run(self):
        """
        Starts the blocking audio stream.
        """
        print("\n🎛️  Initializing Audio Engine...")
        print(f"   Input Device ID: {audio_config.INPUT_DEVICE}")
        print(f"   Output Device ID: {audio_config.OUTPUT_DEVICE}")
        print(f"   Sample Rate: {audio_config.SAMPLE_RATE} Hz")
        print(f"   Block Size: {audio_config.BLOCK_SIZE}")
        
        # Helpful info for user
        # print("   Available Devices:")
        # print(sd.query_devices())
        
        try:
            if self.clean_recorder:
                self.clean_recorder.start()
            if self.fx_recorder:
                self.fx_recorder.start()

            # Start the stream
            # We use settings from audio_config directly
            with sd.Stream(
                device=(audio_config.INPUT_DEVICE, audio_config.OUTPUT_DEVICE),
                channels=2,
                callback=self._audio_callback,
                samplerate=audio_config.SAMPLE_RATE,
                blocksize=audio_config.BLOCK_SIZE
                # latency is handled by sd.default.latency which we set in audio_config
            ):
                print("\n🚀 Pedalboard Running! Press 'Enter' to stop...")
                input()
                
        except Exception as e:
            print(f"\n❌ Audio Engine Error: {e}")
            print("   Tip: Check your device IDs in audio_config.py")
        finally:
            self._save_recordings()

    def _save_recordings(self):
        """
        Saves any active recordings on shutdown.
        """
        if self.clean_recorder or self.fx_recorder:
            print("\n💾 Saving recordings...")
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S.%f")[:18]
            
            if self.clean_recorder:
                self.clean_recorder.save(timestamp=timestamp, suffix="-clean")
            if self.fx_recorder:
                self.fx_recorder.save(timestamp=timestamp, suffix="-fx")
