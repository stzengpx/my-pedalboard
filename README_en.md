# 🎸 My Pedalboard

A realtime guitar effects processor built with Python! Transform your guitar sound with customizable effect chains, all running locally on your Mac.

Built on [Spotify's Pedalboard library](https://github.com/spotify/pedalboard), this project lets you experiment with audio effects, create custom DSP algorithms, and even integrate VST3 plugins.

## ✨ Features

- **Realtime Audio Processing** - Low latency (~10ms) guitar effect processing
- **Multiple Effect Types** - Built-in effects (Reverb, Distortion, Chorus, etc.), custom Python effects, and VST3 plugin support
- **Recording Capability** - Capture both clean and processed audio simultaneously
- **Easy Configuration** - Simple Python-based effect chain configuration
- **Extensible** - Write your own custom effects in Python

## 🚀 Quick Start (MacOS)

### Prerequisites

1. **MacOS** (Intel or Apple Silicon)
2. **Python 3.12+** - Check your version:
   ```bash
   python3 --version
   ```
   If you don't have Python, install it via [Homebrew](https://brew.sh/):
   ```bash
   brew install python3
   ```

3. **Audio Interface** (Recommended) - Any USB audio interface for guitar input
   - Example: Focusrite Scarlett, Spark 2, or similar

### Recommended Development Environment

We recommend using **[Google Antigravity](https://antigravity.google)** for development:
- AI-powered coding assistance
- Browser-based, no local setup needed
- Perfect for vibe coding and experimentation
- Great for engineers who want to focus on creativity, not configuration

### Installation

1. **Clone this repository:**
   ```bash
   git clone https://github.com/stzengpx/my-pedalboard.git
   cd my-pedalboard
   ```

2. **Install dependencies:**
   ```bash
   pip3 install -r requirements.txt
   ```

3. **Find your audio device IDs:**
   ```bash
   python3 -m sounddevice
   ```
   Look for your audio interface in the list and note the device ID numbers.

4. **Configure audio devices:**
   Edit `audio_config.py` and update:
   ```python
   INPUT_DEVICE = 1   # Your audio interface input ID
   OUTPUT_DEVICE = 5  # Your output device ID (speakers/headphones)
   ```

### Running the Pedalboard

**Basic usage** (no recording):
```bash
python3 main.py
```

**With recording** (saves both clean and processed audio):
```bash
python3 main.py -r
```

Press `Enter` to stop the pedalboard. Recordings will be saved to the `output/` directory.

## 🎛️ Built-in Effects

The following effects are available out-of-the-box (no additional plugins required):

### Guitar & Modulation
- **Chorus** - Rich, swirling modulation
- **Distortion** - Overdrive and distortion tones
- **Phaser** - Classic phase-shifting effect

### Dynamics
- **Compressor** - Dynamic range control
- **Gain** - Volume boost/cut
- **Limiter** - Prevent clipping

### EQ & Filters
- **HighpassFilter** - Remove low frequencies
- **LowpassFilter** - Remove high frequencies
- **LadderFilter** - Moog-style multimode filter

### Space & Time
- **Delay** - Echo effects
- **Reverb** - Room ambience
- **Convolution** - Impulse response-based amp/space simulation

### Pitch & Tone
- **PitchShift** - Change pitch without affecting tempo

### Lo-fi & Character
- **GSMFullRateCompressor** - Vintage phone call distortion
- **MP3Compressor** - MP3 compression artifacts
- **Resample** - Bit-crush and sample rate reduction

### Utilities
- **Mix** - Blend multiple effect chains

## ⚙️ Customizing Your Effect Chain

Edit `fx_config.py` to change your effect chain:

```python
PLUGIN_CHAIN_CONFIG = [
    {"type": "internal", "name": "Distortion", "params": {"drive_db": 25}},
    {"type": "internal", "name": "Reverb", "params": {"room_size": 0.8}},
    {"type": "internal", "name": "Gain", "params": {"gain_db": -3}},
]
```

**Pro tip:** Start simple with 1-2 effects, then build up your chain!

## 🛠️ Advanced Usage

### Creating Custom Effects

Add your own DSP effects in `fx_custom.py`:

```python
class MyCustomEffect:
    def __init__(self, param1=1.0):
        self.param1 = param1

    def __call__(self, input_array, sample_rate):
        # Your DSP code here
        return processed_audio
```

Then use it in `fx_config.py`:
```python
{"type": "custom", "name": "MyCustomEffect", "params": {"param1": 2.0}}
```

### Using VST3 Plugins

Install VST3 plugins (optional):
```bash
brew install surge-xt  # Free synthesizer and effects suite
```

Add to your chain:
```python
{"type": "vst3", "path": "/Library/Audio/Plug-Ins/VST3/Surge XT.vst3"}
```

Find more free VST3 plugins:
- [Surge XT](https://surge-synthesizer.github.io/)
- [Vital](https://vital.audio/)
- [TAL Effects](https://tal-software.com/)

## 📂 Project Structure

```
main.py              # Entry point - start here
audio_config.py      # Audio device and performance settings
fx_config.py         # Define your effect chain here
fx_custom.py         # Write custom Python effects
audio_engine.py      # Realtime audio processing
plugin_manager.py    # Effect loading system
mod_aud_rec.py      # Recording functionality
output/             # Recorded audio files go here
```

## 🎯 Future Ideas

From the community:
- **Looper** - Record and loop guitar phrases (Jerry's idea)
- **Auto-tune to Key** - Quantize notes to a specific scale (張永承's idea)
- MIDI controller support
- Real-time parameter automation
- Mobile app interface

Feel free to contribute and add these features!

## 🤔 Technical Notes

### About Latency

Professional guitar pedals typically use C++ with frameworks like JUCE to achieve ultra-low latency (<5ms). This Python implementation targets ~10ms latency, which is acceptable for most playing styles. The tradeoff:

- **Python Pros:** Easy to code, rapid prototyping, great for learning DSP
- **Python Cons:** Higher latency than C++ due to interpreted nature and garbage collection

For most players, 10ms latency is imperceptible. If you need lower latency, consider dedicated hardware pedals or C++ implementations.

### Performance Tips

- Lower `BLOCK_SIZE` in `audio_config.py` for lower latency (at cost of CPU)
- Keep effect chains short (3-5 effects) for best performance
- Built-in Pedalboard effects (C++) are faster than custom Python effects
- Close other audio applications to reduce system load

## 📚 Resources

- [Spotify Pedalboard Documentation](https://spotify.github.io/pedalboard/)
- [Audio Programming in Python](https://realpython.com/playing-and-recording-sound-python/)
- [Digital Signal Processing Basics](https://jackschaedler.github.io/circles-sines-signals/)

## 🤝 Contributing

This project is perfect for vibe coding! Whether you're a seasoned engineer or just starting out:

1. Fork the repo
2. Create a new effect or feature
3. Test it with your guitar
4. Submit a pull request

No contribution is too small - bug fixes, documentation improvements, and new effects are all welcome!

## 📝 License

This project is licensed under the [GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.en.html).

---

**Happy jamming! 🎵**