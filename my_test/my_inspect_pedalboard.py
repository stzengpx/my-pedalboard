
import pedalboard
import inspect
import json

def get_plugin_info():
    plugins = []
    for name, obj in inspect.getmembers(pedalboard):
        if inspect.isclass(obj) and issubclass(obj, pedalboard.Plugin) and obj is not pedalboard.Plugin:
            # Skip some internal or base classes if needed, but pedalboard.Plugin is the main one
            # Check if it has an __init__ method
            try:
                sig = inspect.signature(obj.__init__)
            except ValueError:
                continue
            
            params = []
            for param_name, param in sig.parameters.items():
                if param_name == 'self':
                    continue
                default = param.default
                if default == inspect.Parameter.empty:
                    default_val = "Required"
                else:
                    default_val = str(default)
                
                params.append({
                    "name": param_name,
                    "default": default_val,
                    "annotation": str(param.annotation) if param.annotation != inspect.Parameter.empty else "Any"
                })
            
            plugins.append({
                "name": name,
                "doc": obj.__doc__,
                "params": params
            })
    
    return plugins

if __name__ == "__main__":
    plugin_info = get_plugin_info()
    print(json.dumps(plugin_info, indent=2))
