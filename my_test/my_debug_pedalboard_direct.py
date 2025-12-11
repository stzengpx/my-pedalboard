import pedalboard
import numpy as np

def test_raw_shifter():
    print("Testing raw pedalboard.PitchShift...")
    shifter = pedalboard.PitchShift(semitones=-12)
    sample_rate = 32000
    chunk_size = 1024
    
    # Create random noise input
    input_chunk = np.random.rand(2, chunk_size).astype(np.float32)
    
    total_input = 0
    total_output = 0
    
    for i in range(20):
        output = shifter(input_chunk, sample_rate=sample_rate, reset=True)
        out_samples = output.shape[1]
        print(f"Call {i}: Input {chunk_size} -> Output {out_samples}")
        total_input += chunk_size
        total_output += out_samples
        
    print(f"Total Input: {total_input}")
    print(f"Total Output: {total_output}")
    print(f"Latency/Loss: {total_input - total_output}")

if __name__ == "__main__":
    test_raw_shifter()
