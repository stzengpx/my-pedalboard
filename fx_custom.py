import numpy as np

# --- Custom Effect Library ---

class MyChorus:
    """
    A simple Python implementation of a Vibrato/Chorus effect.
    Uses a circular buffer to create a modulated delay.
    """
    def __init__(self, depth_ms=2.0, speed_hz=2.0, mix=0.5):
        self.depth_ms = depth_ms
        self.speed_hz = speed_hz
        self.mix = mix

        # Buffer setup (assuming 32000Hz or standard rate)
        # We don't have global SAMPLE_RATE here, so we might need it passed in __call__
        # or initialized better. For now, we assume calling context handles state,
        # but standard DSP classes usually need explicit sample rate in init or call.
        # The design in main.py passes sample_rate to __call__, so we rely on that for calculations,
        # but buffer allocation needs a max size.
        # Let's allocate liberally for 48kHz to be safe.
        self.max_sample_rate = 48000
        self.buffer_size = int(self.max_sample_rate * 0.05)
        self.buffer = np.zeros((self.buffer_size, 2)) # Stereo
        self.write_ptr = 0
        self.phase = 0.0

    def __call__(self, input_array, sample_rate):
        # input_array shape: (num_samples, channels)
        num_samples = input_array.shape[0]
        output_array = np.zeros_like(input_array)

        for i in range(num_samples):
            # Write to buffer
            self.buffer[self.write_ptr] = input_array[i]

            # Calculate LFO (Low Frequency Oscillator)
            t = self.phase / sample_rate
            lfo = np.sin(2 * np.pi * self.speed_hz * t)

            # Calculate delay in samples
            delay_ms = 5.0 + (lfo * self.depth_ms) # Base delay 5ms + modulation
            delay_samples = delay_ms * (sample_rate / 1000.0)

            # Read from buffer (Linear Interpolation could be added for quality)
            # Here we just round to nearest integer for speed
            read_ptr = int(self.write_ptr - delay_samples) % self.buffer_size

            wet_signal = self.buffer[read_ptr]

            # Mix dry and wet
            output_array[i] = (input_array[i] * (1 - self.mix)) + (wet_signal * self.mix)

            # Advance pointers
            self.write_ptr = (self.write_ptr + 1) % self.buffer_size
            self.phase += 1

        return output_array


class MyShifter:
    """
    A low-latency Time-Domain Granular Pitch Shifter.
    Uses a dual-tap modulated delay line approach to shift pitch in real-time
    without the high latency or block-size constraints of FFT-based shifters.
    """
    def __init__(self, semitones: float = -12.0, mix: float = 1.0, window_ms: float = 30.0):
        self.semitones = semitones
        self.mix = mix
        
        # Audio Engine params (assumed constant for allocation)
        # We'll adapt in __call__ if sample_rate changes, but init needs a guess
        self.max_buffer_size = 16000 # Enough for generous window
        self.buffer = np.zeros((self.max_buffer_size, 2))
        self.write_ptr = 0
        
        # Shifter State
        self.window_ms = window_ms
        self.phase = 0.0 # 0.0 to 1.0, tracking the delay sweep position
        
        # Pre-calc
        self._update_params(semitones)

    def _update_params(self, semitones):
        # Ratio = 2^(semitones/12)
        # Delay Rate = 1.0 - Ratio
        # If Ratio = 0.5 (-12st), Rate = 0.5 (Delay grows 0.5 samp/samp)
        # If Ratio = 2.0 (+12st), Rate = -1.0 (Delay shrinks 1 samp/samp)
        self.pitch_ratio = 2.0 ** (semitones / 12.0)
        self.delay_rate = 1.0 - self.pitch_ratio

    def __call__(self, input_array, sample_rate):
        # input_array: (block_size, channels)
        num_samples = input_array.shape[0]
        channels = input_array.shape[1]
        
        # 1. Update params if needed (could be dynamic later)
        if hasattr(self, 'current_semitones') and self.current_semitones != self.semitones:
             self._update_params(self.semitones)
             self.current_semitones = self.semitones
        
        # 2. Manage Window
        window_len = int(sample_rate * (self.window_ms / 1000.0))
        if window_len < 1: window_len = 1
        half_window = window_len / 2.0
        
        # 3. Write to circular buffer
        # For simplicity in python, we might just write sequentially and wrap indices later
        indices = np.arange(num_samples) + self.write_ptr
        wrapped_indices = indices % self.max_buffer_size
        
        # Handle wrap-around writing (split into two chunks if needed)
        # But numpy fancy indexing handles this if we just pass a list of indices? 
        # Actually standard fancy indexing allocates a copy.
        # Direct assignment is faster:
        # We can just iterate or use robust slicing. Given small blocks (32), 
        # it rarely wraps.
        for i in range(num_samples):
             self.buffer[(self.write_ptr + i) % self.max_buffer_size] = input_array[i]
             
        # 4. Calculate Delay Trajectories
        # Phase runs 0->1. We map this to 0->WindowLen
        # We need a vector of phases for the block
        # phase_step per sample = delay_rate / window_len ?
        # No.
        # Delay(t) increases by `delay_rate` every sample.
        # When Delay > WindowLen, it wraps.
        # So Normalized Phase step = delay_rate / window_len
        
        phase_step = self.delay_rate / window_len
        
        # Vector of phases for this block
        phases = self.phase + np.arange(num_samples) * phase_step
        
        # Update state for next block (keep it wrapped 0-1)
        self.phase = (phases[-1] + phase_step) % 1.0
        
        # Wrap phases for calculations
        phases = phases % 1.0
        
        # Tap 1 and Tap 2 (180 deg out of phase)
        # Delays in Samples
        delay_1 = phases * window_len
        delay_2 = (phases + 0.5) % 1.0 * window_len
        
        # Windowing Gain (Triangle window)
        # Gain is 1.0 at center (phase 0.5), 0.0 at edges (phase 0.0/1.0)
        # Triangle: 1 - 2*|phase - 0.5|
        gain_1 = 1.0 - 2.0 * np.abs(phases - 0.5)
        gain_2 = 1.0 - 2.0 * np.abs((phases + 0.5) % 1.0 - 0.5)
        
        # 5. Read from Buffer
        # write_ptr points to "now" (or rather, the index we just wrote to is write_ptr + i)
        # Read Index = Write Index - Delay
        # Since we vectorized the write, the "current write index" for sample i is (start_write + i)
        
        current_write_indices = (self.write_ptr + np.arange(num_samples))
        
        # Read Indices
        r_idx_1 = (current_write_indices - delay_1) % self.max_buffer_size
        r_idx_2 = (current_write_indices - delay_2) % self.max_buffer_size
        
        # Nearest Neighbor Interpolation (floor)
        r_idx_1 = r_idx_1.astype(int)
        r_idx_2 = r_idx_2.astype(int)
        
        signal_1 = self.buffer[r_idx_1] # (num_samples, 2)
        signal_2 = self.buffer[r_idx_2]
        
        # Apply Gains (broadcast over channels)
        wet_signal = (signal_1 * gain_1[:, np.newaxis]) + (signal_2 * gain_2[:, np.newaxis])
        
        # 6. Mix
        output_array = (input_array * (1.0 - self.mix)) + (wet_signal * self.mix)
        
        # Advance Write Ptr
        self.write_ptr = (self.write_ptr + num_samples) % self.max_buffer_size
        
        return output_array
