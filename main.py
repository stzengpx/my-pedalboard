import sounddevice as sd
from pedalboard import Pedalboard, Chorus, Reverb, Distortion, Gain, load_plugin
import numpy as np
import soundfile as sf
import argparse
import os
from datetime import datetime
import queue
import fx_custom  # Import the custom module
import fx_config # Import the config module
from mod_aud_rec import AudioRecorder # Import recorder
import audio_config # Import audio settings

def load_effect_chain(config):
    """
    Load effects based on a configuration list.
    Supports 'internal' effects (pedalboard built-ins), 'vst3' plugins, and 'custom' python classes.
    """
    chain = []
    print("🔌 Loading effects chain...")
    
    for item in config:
        try:
            if item["type"] == "internal":
                # Dynamically instantiate internal pedalboard classes by name
                effect_class = globals().get(item["name"])
                if effect_class:
                    params = item.get("params", {})
                    effect = effect_class(**params)
                    chain.append(effect)
                    print(f"   ✅ Loaded Internal: {item['name']}")
                else:
                    print(f"   ⚠️ Unknown internal effect: {item['name']}")
            
            elif item["type"] == "vst3":
                path = item["path"]
                if os.path.exists(path):
                    effect = load_plugin(path)
                    chain.append(effect)
                    print(f"   ✅ Loaded VST3: {os.path.basename(path)}")
                else:
                    print(f"   ⚠️ VST3 not found: {path} (Skipping)")

            elif item["type"] == "custom":
                # Load custom python class from fx_custom module
                effect_class = getattr(fx_custom, item["name"], None)
                if effect_class:
                    params = item.get("params", {})
                    effect = effect_class(**params)
                    chain.append(effect)
                    print(f"   ✅ Loaded Custom: {item['name']}")
                else:
                    print(f"   ⚠️ Unknown custom effect in fx_custom.py: {item['name']}")
                    
        except Exception as e:
            print(f"   ❌ Failed to load {item}: {e}")
            
    return chain

class GuitarPedalboard:
    def __init__(self, clean_recorder=None, fx_recorder=None, plugin_chain=None):
        self.clean_recorder = clean_recorder
        self.fx_recorder = fx_recorder
        
        # Use provided chain or empty list
        if plugin_chain is None:
            self.chain = []
        else:
            self.chain = plugin_chain
            
        # Detect custom effects by checking module name
        # We need a robust way to check if an object is from fx_custom
        self.chain_has_custom = False
        for effect in self.chain:
            if hasattr(effect, '__class__') and effect.__class__.__module__ == 'fx_custom':
                self.chain_has_custom = True
                break

    def callback(self, indata, outdata, frames, time, status):
        """定義回呼函數 (Callback)，這是音訊處理的核心"""
        if status:
            print(status)
        
        # Record the INPUT sound (raw)
        if self.clean_recorder:
            self.clean_recorder.add_frame(indata)

        # Process Audio Chain
        current_signal = indata
        
        try:
            for effect in self.chain:
                # Check if effect is a standard Pedalboard plugin
                # We check this by seeing if it's NOT a custom python effect
                # Or check if it has the C++ interface. 
                # Simplest is: if it's from fx_custom, treat as custom.
                
                if hasattr(effect, '__class__') and effect.__class__.__module__ == 'fx_custom':
                     # Our custom effect expects (samples, channels)
                    current_signal = effect(current_signal, audio_config.SAMPLE_RATE)
                else:
                    # Pedalboard effects (Internal/VST3) need transposition
                    current_signal = effect(current_signal.T, sample_rate=audio_config.SAMPLE_RATE).T

        except Exception as e:
            # If processing fails (e.g. NaN, shape mismatch), pass through silence or dry
            print(f"DSP Error: {e}")
        
        # 将處理後的聲音寫入輸出
        outdata[:] = current_signal

        # Record the OUTPUT sound (fx)
        if self.fx_recorder:
            self.fx_recorder.add_frame(outdata)

    def run(self):
        """啟動音訊串流"""
        print(sd.query_devices())
        
        try:
            if self.clean_recorder:
                self.clean_recorder.start()
            if self.fx_recorder:
                self.fx_recorder.start()

            with sd.Stream(device=(1, 5), channels=2, callback=self.callback, samplerate=audio_config.SAMPLE_RATE, blocksize=audio_config.BLOCK_SIZE):
                print("🎸 吉他效果器已啟動！按 Enter 鍵停止...")
                input()
        except Exception as e:
            print(f"發生錯誤: {e}")
        finally:
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S.%f")[:18]
            
            if self.clean_recorder:
                self.clean_recorder.save(timestamp=timestamp, suffix="-clean")
            if self.fx_recorder:
                self.fx_recorder.save(timestamp=timestamp, suffix="-fx")

def parse_arguments():
    parser = argparse.ArgumentParser(description="Guitar Pedalboard with Recording")
    parser.add_argument("-r", "--record", action="store_true", help="Record both clean and FX sounds")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()
    
    # --- Configuration ---
    # Load configuration from fx_config
    PLUGIN_CHAIN_CONFIG = fx_config.PLUGIN_CHAIN_CONFIG
    # ---------------------
    
    loaded_plugin_chain = load_effect_chain(PLUGIN_CHAIN_CONFIG)
    
    clean_recorder = None
    fx_recorder = None
    
    if args.record:
        clean_recorder = AudioRecorder(audio_config.SAMPLE_RATE)
        fx_recorder = AudioRecorder(audio_config.SAMPLE_RATE)
        
    pedalboard_app = GuitarPedalboard(
        clean_recorder=clean_recorder, 
        fx_recorder=fx_recorder,
        plugin_chain=loaded_plugin_chain
    )
    pedalboard_app.run()
