import sounddevice as sd

SAMPLE_RATE = 32000
BLOCK_SIZE = 64
LATENCY = (0.01, 0.01) # (input, output) ms

# Apply global settings if imported
sd.default.latency = LATENCY
