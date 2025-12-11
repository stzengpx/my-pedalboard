import os
import importlib
import inspect

# Dynamic Import Logic
# This scans the current directory for files starting with 'fx_', imports them,
# and exposes their classes at the package level.
# This way, adding a new fx file automatically makes it available via 'import fx_custom'.

current_dir = os.path.dirname(__file__)

for filename in os.listdir(current_dir):
    if filename.startswith("fx_") and filename.endswith(".py"):
        module_name = filename[:-3] # strip .py
        
        # Import the module
        module = importlib.import_module(f".{module_name}", package=__name__)
        
        # Inspect module for classes
        for name, obj in inspect.getmembers(module):
             if inspect.isclass(obj) and obj.__module__ == module.__name__:
                 # Export class to package namespace
                 globals()[name] = obj

# Clean up namespace
del os, importlib, inspect, current_dir, filename
