import numpy as np

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
