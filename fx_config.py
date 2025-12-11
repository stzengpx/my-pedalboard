class PluginConfig:
    """
    Encapsulates the configuration for a single plugin.
    """
    def __init__(self, type_name: str, name: str = None, path: str = None, params: dict = None):
        self.type = type_name
        self.name = name
        self.path = path
        self.params = params if params else {}

    def to_dict(self):
        config = {"type": self.type, "params": self.params}
        if self.name:
            config["name"] = self.name
        if self.path:
            config["path"] = self.path
        return config

class PedalboardConfig:
    """
    Manages the default effect chain configuration.
    """
    def __init__(self):
        self.chain = []

    def add_internal(self, name: str, params: dict = None):
        self.chain.append(PluginConfig("internal", name=name, params=params))
        return self

    def add_vst3(self, path: str, params: dict = None):
        self.chain.append(PluginConfig("vst3", path=path, params=params))
        return self

    def add_custom(self, name: str, params: dict = None):
        self.chain.append(PluginConfig("custom", name=name, params=params))
        return self

    def get_config_list(self):
        return [plugin.to_dict() for plugin in self.chain]

# config Instance
PLUGIN_CHAIN_CONFIG = [
# PLUGIN_CHAIN_CONFIG_TurnOff = [
    # {"type": "custom", "name": "MyChorus", "params": {"depth_ms": 3.0, "speed_hz": 2.5, "mix": 0.5}},
    # {"type": "custom", "name": "MyShifter", "params": {"semitones": -12.0, "mix": 1.0}}, # Octave Down
    {"type": "internal", "name": "Compressor", "params": {"threshold_db": -12.0, "ratio": 2.5, "attack_ms": 10.0, "release_ms": 100.0}},
    {"type": "internal", "name": "Chorus", "params": {"rate_hz": 0.5, "depth": 0.15, "centre_delay_ms": 7.0, "feedback": 0.0, "mix": 0.3}},
    {"type": "internal", "name": "Reverb", "params": {"room_size": 0.3, "wet_level": 0.3, "dry_level": 1.0}},
    {"type": "internal", "name": "Gain", "params": {"gain_db": 3.0}},
]

# --------------------------------------------------------------------------------
# Specific Tone Demos
# --------------------------------------------------------------------------------

# 1. CleanTone: Fender Strat neck+middle sweet clean
# Needs compression for smoothness, a touch of reverb, and maybe subtle chorus for width.
PLUGIN_CHAIN_CONFIG_DEMO_CleanTone = [
# PLUGIN_CHAIN_CONFIG = [
    {"type": "internal", "name": "Compressor", "params": {"threshold_db": -12.0, "ratio": 2.5, "attack_ms": 10.0, "release_ms": 100.0}},
    {"type": "internal", "name": "Chorus", "params": {"rate_hz": 0.5, "depth": 0.15, "centre_delay_ms": 7.0, "feedback": 0.0, "mix": 0.3}},
    {"type": "internal", "name": "Reverb", "params": {"room_size": 0.3, "wet_level": 0.3, "dry_level": 1.0}},
    {"type": "internal", "name": "Gain", "params": {"gain_db": 3.0}},
]

# 2. LeadGuitar: Metal style, high output
# Needs NoiseGate, High Gain Distortion, and Delay for solos.
PLUGIN_CHAIN_CONFIG_DEMO_LeadGuitar = [
# PLUGIN_CHAIN_CONFIG = [
    {"type": "internal", "name": "NoiseGate", "params": {"threshold_db": -50.0}},
    {"type": "internal", "name": "Distortion", "params": {"drive_db": 30.0}}, # High gain
    {"type": "internal", "name": "Delay", "params": {"delay_seconds": 0.35, "feedback": 0.3, "mix": 0.4}},
    {"type": "internal", "name": "Reverb", "params": {"room_size": 0.1, "wet_level": 0.2}}, # Small room for tightness
    {"type": "internal", "name": "Gain", "params": {"gain_db": 2.0}},
]

# 3. SoloGuitar: Singing tone, ear-catching
# Smooth sustain (Compressor + Distortion), creamy Delay, larger Reverb for size.
PLUGIN_CHAIN_CONFIG_DEMO_SoloGuitar = [
# PLUGIN_CHAIN_CONFIG = [
    {"type": "internal", "name": "Compressor", "params": {"threshold_db": -15.0, "ratio": 4.0, "attack_ms": 5.0, "release_ms": 200.0}}, # Sustain
    {"type": "internal", "name": "Distortion", "params": {"drive_db": 18.0}}, # Singing drive, not too fizzy
    {"type": "internal", "name": "Delay", "params": {"delay_seconds": 0.45, "feedback": 0.4, "mix": 0.5}}, # Ambient delay
    {"type": "internal", "name": "Reverb", "params": {"room_size": 0.7, "wet_level": 0.4}}, # Big hall presence
]

# 4. Crunch: Strumming, accompaniment
# Light breakup, dynamic.
PLUGIN_CHAIN_CONFIG_DEMO_Crunch = [
# PLUGIN_CHAIN_CONFIG = [
    {"type": "internal", "name": "Compressor", "params": {"threshold_db": -10.0, "ratio": 2.0}}, # Light glue
    {"type": "internal", "name": "Distortion", "params": {"drive_db": 12.0}}, # Edge of breakup
    {"type": "internal", "name": "Reverb", "params": {"room_size": 0.4, "wet_level": 0.25}},
    {"type": "internal", "name": "Gain", "params": {"gain_db": 0.0}},
]
