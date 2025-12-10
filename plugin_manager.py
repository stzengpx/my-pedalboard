import os
import pedalboard
from pedalboard import load_plugin
import fx_custom

class PluginManager:
    """
    Responsible for loading plugins/effects from configuration.
    Implements a simple Factory Pattern to instantiate different types of effects.
    """

    @staticmethod
    def load_effect_chain(config: list) -> list:
        """
        Parses the configuration list and returns a list of instantiated effect objects.
        """
        chain = []
        print("🔌 Loading effects chain...")

        for item in config:
            try:
                plugin_type = item.get("type")
                name = item.get("name")
                params = item.get("params", {})

                if plugin_type == "internal":
                    effect = PluginManager._load_internal(name, params)
                elif plugin_type == "vst3":
                    path = item.get("path")
                    effect = PluginManager._load_vst3(path)
                elif plugin_type == "custom":
                    effect = PluginManager._load_custom(name, params)
                else:
                    print(f"   ⚠️ Unknown plugin type: {plugin_type} for {name}")
                    continue

                if effect:
                    chain.append(effect)
                    label = name if name else os.path.basename(item.get("path", "Unknown"))
                    print(f"   ✅ Loaded {plugin_type.capitalize()}: {label}")

            except (ImportError, AttributeError, TypeError) as e:
                print(f"   ❌ Failed to load {item}: {e}")

        return chain

    @staticmethod
    def _load_internal(name: str, params: dict):
        # Dynamically import pedalboard checks globals of where this is called?
        # No, we need to import them here or assume they are available.
        # Ideally, we explicitly import the supported classes to avoid arbitrary code execution,
        # but for flexibility we can check the pedalboard module.

        # Check if the class exists in the pedalboard module
        effect_class = getattr(pedalboard, name, None)
        if effect_class:
            return effect_class(**params)
        print(f"   ⚠️ Unknown internal effect class: {name}")
        return None

    @staticmethod
    def _load_vst3(path: str):
        if path and os.path.exists(path):
            return load_plugin(path)
        print(f"   ⚠️ VST3 not found: {path} (Skipping)")
        return None

    @staticmethod
    def _load_custom(name: str, params: dict):
        effect_class = getattr(fx_custom, name, None)
        if effect_class:
            return effect_class(**params)
        print(f"   ⚠️ Unknown custom effect class in fx_custom: {name}")
        return None
