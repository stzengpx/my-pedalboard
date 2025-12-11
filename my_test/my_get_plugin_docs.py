
import pedalboard
import inspect
import json

def get_plugin_docs():
    plugins = ["Chorus", "Reverb", "Distortion", "Gain"]
    docs = {}
    for name in plugins:
        if hasattr(pedalboard, name):
            obj = getattr(pedalboard, name)
            docs[name] = {
                "class_doc": obj.__doc__,
                "init_doc": obj.__init__.__doc__
            }
    return docs

if __name__ == "__main__":
    print(json.dumps(get_plugin_docs(), indent=2))
