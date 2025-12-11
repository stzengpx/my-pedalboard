import pedalboard
import numpy as np

def test_streaming_board():
    print("Testing streaming with Pedalboard wrapper...")
    
    # Create the board
    shifter = pedalboard.PitchShift(semitones=-12)
    board = pedalboard.Pedalboard([shifter])
    
    sample_rate = 32000
    chunk_size = 512 # Reasonable size
    
    # 2 seconds of noise
    total_samples = 32000 * 2
    input_signal = np.random.rand(2, total_samples).astype(np.float32)
    
    # Process in chunks
    cursor = 0
    total_energy = 0
    chunks_processed = 0
    
    while cursor < total_samples:
        end = min(cursor + chunk_size, total_samples)
        chunk = input_signal[:, cursor:end]
        
        # Using board.process with reset=False implicitly?
        # board.process signature: (input_array, sample_rate, buffer_size=8192, reset=True)
        # We set reset=False
        output = board.process(chunk, sample_rate=sample_rate, reset=False)
        
        energy = np.sum(np.abs(output))
        total_energy += energy
        chunks_processed += 1
        
        if chunks_processed < 5:
             print(f"Chunk {chunks_processed}: Input {chunk.shape[1]} -> Output {output.shape[1]}, Energy: {energy}")
             
        cursor = end
        
    print(f"Total processed: {chunks_processed} chunks")
    print(f"Total Energy: {total_energy}")
    
    if total_energy == 0:
        print("❌ Still Silent with Pedalboard wrapper.")
    else:
        print("✅ Sound detected with Pedalboard wrapper!")

if __name__ == "__main__":
    test_streaming_board()
