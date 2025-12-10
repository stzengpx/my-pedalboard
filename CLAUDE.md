# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A Python-based realtime guitar pedalboard application built on Spotify's Pedalboard library. Processes audio input through configurable effect chains with sub-10ms latency for live performance. Supports internal effects (from Pedalboard), custom Python DSP effects, and VST3 plugins.

## Development Commands

**Setup:**
```bash
pip install -r requirements.txt
```

**Run the application:**
```bash
python main.py              # Run pedalboard without recording
python main.py -r           # Run with recording (saves clean and FX outputs)
```

**List available audio devices:**
```bash
python3 -m sounddevice
```

**VST3 Plugin Installation (optional):**
```bash
brew install surge-xt       # Example VST3 synth/effects suite
```

## Architecture

### Core Components

The application follows a modular architecture with clear separation of concerns:

**main.py** - Entry point that orchestrates initialization:
1. Parses CLI arguments (`-r` for recording)
2. Loads effect chain configuration from `fx_config.py`
3. Instantiates effect chain via `PluginManager`
4. Sets up optional `AudioRecorder` instances (clean + FX)
5. Initializes and runs `PedalboardEngine`

**audio_config.py** - Global audio settings:
- Sample rate, block size, latency settings
- Audio device IDs (input/output)
- Uses `sounddevice` global defaults

**fx_config.py** - Effect chain configuration:
- Defines `PLUGIN_CHAIN_CONFIG` list specifying effect order
- Each effect has `type` (internal/custom/vst3), `name`/`path`, and `params`
- Includes helper classes `PluginConfig` and `PedalboardConfig` for building configs programmatically

**plugin_manager.py** - Effect instantiation (Factory Pattern):
- Loads effect chain from configuration
- Handles three plugin types:
  - `internal`: Pedalboard's built-in C++ effects (Distortion, Reverb, Chorus, etc.)
  - `custom`: Python DSP effects from `fx_custom.py`
  - `vst3`: External VST3 plugins via file path
- Gracefully handles missing plugins

**audio_engine.py** - Realtime audio processing:
- Manages `sounddevice` stream with low-latency callback
- Audio callback flow: clean recording → effect chain processing → output → FX recording
- Handles transpose logic for effect compatibility (custom Python effects use `(samples, channels)`, Pedalboard C++ effects use `(channels, samples)`)
- Saves recordings on shutdown

**mod_aud_rec.py** - Recording functionality:
- Buffers audio frames in memory
- Saves to timestamped MP3 files (falls back to WAV if MP3 encoding unavailable)
- Output directory: `output/`

**fx_custom.py** - Custom Python DSP effects:
- Example: `MyChorus` implements vibrato/chorus using circular buffer and LFO
- Custom effects must implement `__call__(input_array, sample_rate)` interface
- Array format: `(num_samples, channels)` for compatibility with NumPy operations

### Key Design Patterns

**Effect Processing Logic:**
- Custom Python effects are detected via module check: `effect.__class__.__module__ == 'fx_custom'`
- Custom effects: called directly with `(samples, channels)` format
- Pedalboard effects: transposed to `(channels, samples)`, processed, then transposed back

**Configuration vs. Implementation:**
- Effect chains are data-driven via `fx_config.py`
- No code changes needed to reorder effects or adjust parameters
- Easy to experiment with different signal chains

### Audio Device Configuration

Device IDs are hardware-specific. To find your device IDs:
1. Run `python3 -m sounddevice`
2. Update `INPUT_DEVICE` and `OUTPUT_DEVICE` in `audio_config.py`

Default configuration uses:
- INPUT_DEVICE = 1 (e.g., Spark 2 USB Audio)
- OUTPUT_DEVICE = 5 (e.g., MacBook Pro Speakers)

### Available Internal Effects

From Spotify Pedalboard (no VST required):
- **Guitar/Modulation:** Chorus, Distortion, Phaser
- **Dynamics:** Compressor, Gain, Limiter
- **EQ/Filters:** HighpassFilter, LowpassFilter, LadderFilter
- **Space/Time:** Delay, Reverb, Convolution
- **Pitch:** PitchShift
- **Lo-fi:** GSMFullRateCompressor, MP3Compressor, Resample
- **Utility:** Mix (blend multiple chains)

### Performance Considerations

- Sample rate: 32kHz (configurable in `audio_config.py`)
- Block size: 64 samples (~2ms at 32kHz)
- Target latency: 10ms input + 10ms output
- Python effects are slower than C++ Pedalboard effects but acceptable for single effects
- Avoid heavy processing in custom Python effects (complex filters, FFTs, etc.)

## File Organization

```
main.py                 # Entry point
audio_config.py         # Hardware/stream settings
audio_engine.py         # Realtime processing loop
plugin_manager.py       # Effect loading/instantiation
fx_config.py           # Effect chain configuration
fx_custom.py           # Custom Python DSP effects
mod_aud_rec.py         # Recording functionality
requirements.txt       # Dependencies
output/                # Recorded audio files (gitignored)
```

## Adding New Effects

**Internal Pedalboard effect:**
Edit `fx_config.py`:
```python
PLUGIN_CHAIN_CONFIG = [
    {"type": "internal", "name": "Chorus", "params": {"rate_hz": 3.0, "depth": 0.5}},
]
```

**Custom Python effect:**
1. Add class to `fx_custom.py` with `__call__(input_array, sample_rate)` method
2. Reference in `fx_config.py`:
```python
{"type": "custom", "name": "MyChorus", "params": {"depth_ms": 3.0}}
```

**VST3 plugin:**
```python
{"type": "vst3", "path": "/Library/Audio/Plug-Ins/VST3/SomePlugin.vst3", "params": {}}
```

## Known Limitations

- MP3 recording requires libmp3lame (falls back to WAV if unavailable)
- VST3 parameter setting not yet implemented (plugins use default params)
- Custom Python effects must carefully manage buffer allocation for different sample rates
- No MIDI control or parameter automation yet
