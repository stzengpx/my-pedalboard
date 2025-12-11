import numpy as np
import sys
import os

sys.path.append(os.getcwd())

import fx_custom
# Check import
shifter = fx_custom.MyShifter(semitones=-12)
sample_rate = 32000
block_size = 32

# Test shape handling logic simulation
# Assuming audio_engine passes (block, channels)
# Let's verify our MyShifter call logic matches expectation
input_block = np.zeros((block_size, 2))
try:
    output = shifter(input_block, sample_rate)
    print(f"Shape In: {input_block.shape}, Shape Out: {output.shape}")
    if output.shape == input_block.shape:
        print("✅ MyShifter handles (samples, channels) correctly.")
    else:
        print("❌ MyShifter returned wrong shape.")
except Exception as e:
    print(f"❌ Crash: {e}")
