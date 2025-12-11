
import pedalboard
import inspect
import json
import re

def parse_signature(doc_str):
    if not doc_str:
        return []
    
    # Extract content inside parentheses
    match = re.search(r'__init__\((.*?)\)', doc_str, re.DOTALL)
    if not match:
        return []
    
    params_str = match.group(1)
    # Split by comma, but be careful (simple split might work if no complex types with commas)
    # For this library, types seem simple enough.
    
    # A robust split that handles nested brackets if needed, but let's try simple first
    # Clean up newlines if any
    params_str = params_str.replace('\n', ' ')
    
    raw_params = [p.strip() for p in params_str.split(',')]
    
    parsed_params = []
    for p in raw_params:
        if not p or p == 'self' or p.startswith('self:'):
            continue
            
        # Format: name: type = default  OR  name: type
        parts = p.split('=')
        name_part = parts[0].strip()
        default_val = parts[1].strip() if len(parts) > 1 else "Required"
        
        # Extract name (remove type hint)
        name_match = re.match(r'(\w+)', name_part)
        if name_match:
            name = name_match.group(1)
        else:
            name = name_part # Fallback
            
        parsed_params.append({
            "name": name,
            "default": default_val
        })
        
    return parsed_params


def get_all_plugin_signatures():
    plugin_names = [
        "Bitcrush", "Chorus", "Clipping", "Compressor", "Convolution", 
        "Delay", "Distortion", "GSMFullRateCompressor", "Gain", 
        "HighShelfFilter", "HighpassFilter", "IIRFilter", "Invert", 
        "LadderFilter", "Limiter", "LowShelfFilter", "LowpassFilter", 
        "MP3Compressor", "Mix", "NoiseGate", "PeakFilter", 
        "Phaser", "PitchShift", "Resample", "Reverb"
    ]
    
    results = {}
    
    for name in plugin_names:
        if hasattr(pedalboard, name):
            obj = getattr(pedalboard, name)
            doc = obj.__init__.__doc__
            params = parse_signature(doc)
            results[name] = params
            
    return results

if __name__ == "__main__":
    print(json.dumps(get_all_plugin_signatures(), indent=2))
