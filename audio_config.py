import sounddevice as sd

SAMPLE_RATE = 32000
BLOCK_SIZE = 64
LATENCY = (0.01, 0.01) # (input, output) ms

# Device Selection
# Use `python3 -m sounddevice` to list available devices by ID
INPUT_DEVICE = 1 # e.g. Spark 2 USB Audio
OUTPUT_DEVICE = 5 # e.g. MacBook Pro Speakers

# Apply global settings if imported
sd.default.device = (INPUT_DEVICE, OUTPUT_DEVICE)
sd.default.latency = LATENCY
