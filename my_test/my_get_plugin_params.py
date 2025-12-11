
import pedalboard
import inspect
import json

def get_plugin_params():
    # List of classes to exclude (containers, base classes, etc.)
    excludes = [
        "AudioProcessorParameter",
        "AudioUnitPlugin",
        "Chain", 
        "ExternalPlugin",
        "ExternalPluginReloadType",
        "Pedalboard",
        "Plugin",
        "PluginContainer",
        "VST3Plugin",
        "_klass"
    ]
    
    plugins_data = {}
    
    for name, obj in inspect.getmembers(pedalboard):
        if inspect.isclass(obj) and name not in excludes:
            # Check if it looks like a plugin (inherits from Plugin or has processing methods)
            # The most reliable way for pedalboard native objects might be checking if it's in the module
            # and not in the exclude list, as we did.
            
            try:
                sig = inspect.signature(obj.__init__)
            except ValueError:
                # Some built-in classes might not have a signature accessible via inspect
                # But pedalboard classes usually do or we can't inspect them easily.
                # Let's try to simulate or skip.
                continue
                
            params = {}
            for param_name, param in sig.parameters.items():
                if param_name == 'self':
                    continue
                    
                val_str = str(param.default)
                if val_str == "<class 'inspect._empty'>":
                    val_str = "Required"
                
                # Clean up float values
                if isinstance(param.default, float):
                     val_str = f"{param.default:.2f}".rstrip('0').rstrip('.')
                     
                params[param_name] = val_str
            
            plugins_data[name] = params
            
    return plugins_data

if __name__ == "__main__":
    print(json.dumps(get_plugin_params(), indent=2))
