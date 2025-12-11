import numpy as np
import sys
import os

# Add current directory to path
sys.path.append(os.getcwd())

import fx_custom
import audio_config

def test_shifter_streaming():
    print("Testing MyShifter with streaming (Block Size = 32)...")
    
    sample_rate = 32000
    block_size = 32 # Emulating the user's audio_config
    total_blocks = 2000
    
    # Create input: Sine wave
    t = np.linspace(0, (block_size * total_blocks) / sample_rate, block_size * total_blocks, endpoint=False)
    full_input = np.sin(2 * np.pi * 440 * t) 
    
    # Instantiate Shifter
    # Mix 1.0 to see if wet signal exists
    shifter = fx_custom.MyShifter(semitones=-12, mix=1.0)
    
    non_zero_blocks = 0
    total_energy = 0.0
    
    print(f"Processing {total_blocks} blocks of {block_size} samples...")
    
    for i in range(total_blocks):
        start = i * block_size
        end = start + block_size
        
        # Prepare block (samples, channels)
        block_input = np.zeros((block_size, 2), dtype=np.float32)
        block_input[:, 0] = full_input[start:end]
        block_input[:, 1] = full_input[start:end]
        
        # Process
        block_output = shifter(block_input, sample_rate)
        
        # Check energy
        energy = np.sum(np.abs(block_output))
        total_energy += energy
        if energy > 1e-6:
            non_zero_blocks += 1
            if non_zero_blocks == 1:
                 print(f"First sound detected at block {i}")
    
    print(f"\nResults:")
    print(f"Total Energy: {total_energy}")
    print(f"Blocks with sound: {non_zero_blocks}/{total_blocks}")
    
    if non_zero_blocks == 0:
        print("❌ FAILED: No sound output detected (Silence).")
    else:
         print("✅ PASSED: Sound output detected.")

if __name__ == "__main__":
    test_shifter_streaming()
