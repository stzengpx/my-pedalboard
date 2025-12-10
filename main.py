import argparse
import audio_config
import fx_config
from mod_aud_rec import AudioRecorder
from plugin_manager import PluginManager
from audio_engine import PedalboardEngine

def parse_arguments():
    parser = argparse.ArgumentParser(description="Guitar Pedalboard with Recording")
    parser.add_argument("-r", "--record", action="store_true", help="Record both clean and FX sounds")
    return parser.parse_args()

def main():
    args = parse_arguments()
    
    # 1. Load Configuration
    plugin_config = fx_config.PLUGIN_CHAIN_CONFIG
    
    # 2. Build Effect Chain
    # The PluginManager handles the complexity of creating different types of effects
    plugin_chain = PluginManager.load_effect_chain(plugin_config)
    
    # 3. Setup Recorders (if requested)
    clean_recorder = None
    fx_recorder = None
    
    if args.record:
        # We pass the sample rate so recorders know how to save files correctly
        clean_recorder = AudioRecorder(audio_config.SAMPLE_RATE)
        fx_recorder = AudioRecorder(audio_config.SAMPLE_RATE)
        
    # 4. Initialize and Run Engine
    # The PedalboardEngine handles the realtime audio loop
    engine = PedalboardEngine(
        clean_recorder=clean_recorder, 
        fx_recorder=fx_recorder, 
        plugin_chain=plugin_chain
    )
    
    engine.run()

if __name__ == "__main__":
    main()
