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
    # {"type": "internal", "name": "Distortion", "params": {"drive_db": 25}},
    {"type": "custom", "name": "MyChorus", "params": {"depth_ms": 3.0, "speed_hz": 2.5, "mix": 0.5}},
    {"type": "internal", "name": "Reverb", "params": {"room_size": 0.5}},
    {"type": "internal", "name": "Gain", "params": {"gain_db": -3}},
]
