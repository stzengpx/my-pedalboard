# 🎸 My Pedalboard

一個用 Python 打造的即時吉他效果器！在你的 Mac 上透過可自訂的效果鏈，轉換你的吉他音色。

基於 [Spotify 的 Pedalboard 函式庫](https://github.com/spotify/pedalboard)開發，這個專案讓你可以實驗音訊效果、創造自訂 DSP 演算法，甚至整合 VST3 插件。

## ✨ 特色功能

- **即時音訊處理** - 低延遲（約 10ms）的吉他效果處理
- **多種效果類型** - 內建效果（Reverb、Distortion、Chorus 等）、自訂 Python 效果，以及 VST3 插件支援
- **錄音功能** - 同時錄製乾淨訊號和處理後的音訊
- **簡易設定** - 基於 Python 的簡單效果鏈設定
- **可擴充性** - 用 Python 編寫你自己的客製化效果

## 🚀 快速開始（MacOS）

### 事前準備

1. **MacOS**（Intel 或 Apple Silicon 皆可）
2. **Python 3.12+** - 檢查你的版本：
   ```bash
   python3 --version
   ```
   如果你還沒有 Python，可以透過 [Homebrew](https://brew.sh/) 安裝：
   ```bash
   brew install python3
   ```

3. **音訊介面**（建議）- 任何 USB 音訊介面都可以用來輸入吉他訊號
   - 例如：Focusrite Scarlett、Spark 2 或類似產品
   - 最簡單的應該是 "Type C" 轉 "3.5麥克風 + 3.5耳機"
      - ex: https://24h.pchome.com.tw/prod/DCACH3-A900FY56S

### 推薦開發環境

我們推薦使用 **[Google Antigravity](https://antigravity.google)** 進行開發：
- AI 驅動的程式碼輔助
- 完美適合 vibe coding 和實驗
- 非常適合想專注於創意而非繁瑣設定的工程師/非工程背景的工程師

### 安裝步驟

1. **複製這個專案：**
   ```bash
   git clone https://github.com/stzengpx/my-pedalboard.git
   cd my-pedalboard
   ```

2. **安裝相依套件：**
   ```bash
   pip3 install -r requirements.txt
   ```

3. **找出你的音訊裝置 ID：**
   ```bash
   python3 -m sounddevice
   ```
   在列表中找到你的音訊介面並記下裝置 ID 編號。

4. **設定音訊裝置：**
   編輯 `audio_config.py` 並更新：
   ```python
   INPUT_DEVICE = 1   # 你的音訊介面輸入 ID
   OUTPUT_DEVICE = 5  # 你的輸出裝置 ID（喇叭/耳機）
   ```

### 執行 Pedalboard

**基本使用**（不錄音）：
```bash
python3 main.py
```

**啟用錄音**（同時儲存乾淨訊號和處理後的音訊）：
```bash
python3 main.py -r
```

**使用預設效果鏈**：
```bash
python3 main.py -p a1 # Loading Preset: Clean Tone
python3 main.py -p a2 # Loading Preset: Lead Guitar
python3 main.py -p a3 # Loading Preset: Solo Guitar
python3 main.py -p a4 # Loading Preset: Crunch
```

按下 `Enter` 停止 pedalboard。錄音檔案會儲存在 `output/` 目錄中。

## 🎛️ 內建效果器

以下效果無需額外插件即可使用，參數為預設值：

### 🎚️ 動態 & 音量 (Dynamics & Volume)
- **Compressor** (壓縮器)
  - `threshold_db` (0): 閾值，超過此音量的訊號會被壓縮
  - `ratio` (1): 壓縮比率
  - `attack_ms` (1.0): 啟動時間
  - `release_ms` (100): 釋放時間
- **Limiter** (限幅器)
  - `threshold_db` (-10.0): 限制閾值
  - `release_ms` (100.0): 釋放時間
- **Gain** (增益)
  - `gain_db` (1.0): 增益值 (dB)
- **NoiseGate** (噪音門)
  - `threshold_db` (-100.0): 噪音門開啟閾值
  - `ratio` (10): 衰減比率
  - `attack_ms` (1.0): 啟動時間
  - `release_ms` (100.0): 釋放時間
- **Clipping** (削波)
  - `threshold_db` (-6.0): 削波閾值

### 🌀 調變 (Modulation)
- **Chorus** (合唱)
  - `rate_hz` (1.0): 調變速率
  - `depth` (0.25): 調變深度
  - `centre_delay_ms` (7.0): 中心延遲時間
  - `feedback` (0.0): 回授量
  - `mix` (0.5): 乾濕比
- **Phaser** (相位器)
  - `rate_hz` (1.0): 調變速率
  - `depth` (0.5): 深度
  - `centre_frequency_hz` (1300.0): 中心頻率
  - `feedback` (0.0): 回授
  - `mix` (0.5): 乾濕比

### 🌌 空間 & 時間 (Time & Space)
- **Delay** (延遲)
  - `delay_seconds` (0.5): 延遲時間(秒)
  - `feedback` (0.0): 回授量
  - `mix` (0.5): 乾濕比
- **Reverb** (殘響)
  - `room_size` (0.5): 空間大小
  - `damping` (0.5): 高頻衰減
  - `wet_level` (0.33): 濕訊號音量
  - `dry_level` (0.4): 乾訊號音量
  - `width` (1.0): 立體聲寬度
  - `freeze_mode` (0.0): 凍結模式 (1.0 為開啟)
- **Convolution** (迴旋)
  - `impulse_response_filename`: 脈衝響應檔案路徑 (.wav)
  - `mix` (1.0): 乾濕比

### 🎛️ 濾波器 & EQ (Filters & EQ)
- **HighpassFilter** (高通) / **LowpassFilter** (低通)
  - `cutoff_frequency_hz` (50): 截止頻率
- **HighShelfFilter** / **LowShelfFilter** / **PeakFilter**
  - `cutoff_frequency_hz` (440): 中心/截止頻率
  - `gain_db` (0.0): 增益
  - `q` (0.707): Q 值 (頻寬)
- **LadderFilter** (階梯濾波器)
  - `mode` (0): 濾波模式 (LPF12, LPF24 等)
  - `cutoff_hz` (200): 截止頻率
  - `resonance` (0): 共振
  - `drive` (1.0): 驅動

### 🎸 特殊效果 (Pitch & Distortion)
- **Distortion** (破音)
  - `drive_db` (25): 驅動量
- **PitchShift** (移調)
  - `semitones` (0.0): 半音數 (例如 +12 變高八度)
- **Bitcrush** (位元破碎)
  - `bit_depth` (8): 位元深度 (例如 8-bit)

### 📻 Lo-fi & Codec
- **GSMFullRateCompressor** / **MP3Compressor** / **Resample**
  - 用於模擬低品質音訊或特殊的數位失真質感

### Demo Configuration: Reference for Built-in Effects
- Copy any of these into PLUGIN_CHAIN_CONFIG to use them.
```=python
PLUGIN_CHAIN_CONFIG_DEMO = [
    # --- Dynamics & Volume ---
    {"type": "internal", "name": "Compressor", "params": {"threshold_db": 0, "ratio": 1, "attack_ms": 1.0, "release_ms": 100}},
    {"type": "internal", "name": "Limiter", "params": {"threshold_db": -10.0, "release_ms": 100.0}},
    {"type": "internal", "name": "Gain", "params": {"gain_db": 1.0}},
    {"type": "internal", "name": "NoiseGate", "params": {"threshold_db": -100.0, "ratio": 10, "attack_ms": 1.0, "release_ms": 100.0}},
    {"type": "internal", "name": "Clipping", "params": {"threshold_db": -6.0}},
    
    # --- Modulation ---
    {"type": "internal", "name": "Chorus", "params": {"rate_hz": 1.0, "depth": 0.25, "centre_delay_ms": 7.0, "feedback": 0.0, "mix": 0.5}},
    {"type": "internal", "name": "Phaser", "params": {"rate_hz": 1.0, "depth": 0.5, "centre_frequency_hz": 1300.0, "feedback": 0.0, "mix": 0.5}},
    
    # --- Time & Space ---
    {"type": "internal", "name": "Delay", "params": {"delay_seconds": 0.5, "feedback": 0.0, "mix": 0.5}},
    {"type": "internal", "name": "Reverb", "params": {"room_size": 0.5, "damping": 0.5, "wet_level": 0.33, "dry_level": 0.4, "width": 1.0, "freeze_mode": 0.0}},
    # Convolution requires an impulse response file
    # {"type": "internal", "name": "Convolution", "params": {"impulse_response_filename": "/path/to/ir.wav", "mix": 1.0}},
    
    # --- Filters & EQ ---
    {"type": "internal", "name": "HighpassFilter", "params": {"cutoff_frequency_hz": 50}},
    {"type": "internal", "name": "LowpassFilter", "params": {"cutoff_frequency_hz": 50}},
    {"type": "internal", "name": "HighShelfFilter", "params": {"cutoff_frequency_hz": 440, "gain_db": 0.0, "q": 0.707}},
    {"type": "internal", "name": "LowShelfFilter", "params": {"cutoff_frequency_hz": 440, "gain_db": 0.0, "q": 0.707}},
    {"type": "internal", "name": "PeakFilter", "params": {"cutoff_frequency_hz": 440, "gain_db": 0.0, "q": 0.707}},
    {"type": "internal", "name": "LadderFilter", "params": {"mode": 0, "cutoff_hz": 200, "resonance": 0, "drive": 1.0}},
    # IIRFilter and Invert take no or complex params
    # {"type": "internal", "name": "Invert", "params": {}},
    
    # --- Pitch & Distortion ---
    {"type": "internal", "name": "Distortion", "params": {"drive_db": 25}},
    {"type": "internal", "name": "PitchShift", "params": {"semitones": 0.0}},
    {"type": "internal", "name": "Bitcrush", "params": {"bit_depth": 8}},
    
    # --- Lo-fi / Codec ---
    {"type": "internal", "name": "GSMFullRateCompressor", "params": {"quality": 10}},
    {"type": "internal", "name": "MP3Compressor", "params": {"vbr_quality": 2.0}},
    {"type": "internal", "name": "Resample", "params": {"target_sample_rate": 8000.0, "quality": 8}},
]
```

### 🎸 預設風格範例 (Tone Demos)

你可以直接複製這些設定到 `PLUGIN_CHAIN_CONFIG`！

#### 1. Clean Tone (清甜音色)
適用於 Fender Stratocaster neck/middle pickup，乾淨且帶有空間感。
```python
PLUGIN_CHAIN_CONFIG_DEMO_CleanTone = [
    {"type": "internal", "name": "Compressor", "params": {"threshold_db": -12.0, "ratio": 2.5, "attack_ms": 10.0, "release_ms": 100.0}},
    {"type": "internal", "name": "Chorus", "params": {"rate_hz": 0.5, "depth": 0.15, "centre_delay_ms": 7.0, "feedback": 0.0, "mix": 0.3}},
    {"type": "internal", "name": "Reverb", "params": {"room_size": 0.3, "wet_level": 0.3, "dry_level": 1.0}},
    {"type": "internal", "name": "Gain", "params": {"gain_db": 3.0}},
]
```

#### 2. Lead Guitar (金屬主奏)
高出力、High Gain，搭配 NoiseGate 消除雜訊，適合 Metal Solo。
```python
PLUGIN_CHAIN_CONFIG_DEMO_LeadGuitar = [
    {"type": "internal", "name": "NoiseGate", "params": {"threshold_db": -50.0}},
    {"type": "internal", "name": "Distortion", "params": {"drive_db": 30.0}},
    {"type": "internal", "name": "Delay", "params": {"delay_seconds": 0.35, "feedback": 0.3, "mix": 0.4}},
    {"type": "internal", "name": "Reverb", "params": {"room_size": 0.1, "wet_level": 0.2}},
    {"type": "internal", "name": "Gain", "params": {"gain_db": 2.0}},
]
```

#### 3. Solo Guitar (唱功獨奏)
強調延音 (Sustain) 與歌唱般的音色，適合抓耳的旋律演奏。
```python
PLUGIN_CHAIN_CONFIG_DEMO_SoloGuitar = [
    {"type": "internal", "name": "Compressor", "params": {"threshold_db": -15.0, "ratio": 4.0, "attack_ms": 5.0, "release_ms": 200.0}},
    {"type": "internal", "name": "Distortion", "params": {"drive_db": 18.0}},
    {"type": "internal", "name": "Delay", "params": {"delay_seconds": 0.45, "feedback": 0.4, "mix": 0.5}},
    {"type": "internal", "name": "Reverb", "params": {"room_size": 0.7, "wet_level": 0.4}},
]
```

#### 4. Crunch (節奏伴奏)
適合刷和弦的輕度過載音色，動態豐富。
```python
PLUGIN_CHAIN_CONFIG_DEMO_Crunch = [
    {"type": "internal", "name": "Compressor", "params": {"threshold_db": -10.0, "ratio": 2.0}},
    {"type": "internal", "name": "Distortion", "params": {"drive_db": 12.0}},
    {"type": "internal", "name": "Reverb", "params": {"room_size": 0.4, "wet_level": 0.25}},
    {"type": "internal", "name": "Gain", "params": {"gain_db": 0.0}},
]
```

## ⚙️ 自訂你的效果鏈

編輯 `fx_config.py` 來改變你的效果鏈：

```python
PLUGIN_CHAIN_CONFIG = [
    {"type": "internal", "name": "Distortion", "params": {"drive_db": 25}},
    {"type": "internal", "name": "Reverb", "params": {"room_size": 0.8}},
    {"type": "internal", "name": "Gain", "params": {"gain_db": -3}},
]
```

**小技巧：** 從 1-2 個效果開始，再逐步建構你的效果鏈！

## 🛠️ 進階使用

### 創建自訂效果

在 `fx_custom.py` 中加入你自己的 DSP 效果：

```python
class MyCustomEffect:
    def __init__(self, param1=1.0):
        self.param1 = param1

    def __call__(self, input_array, sample_rate):
        # 你的 DSP 程式碼
        return processed_audio
```

然後在 `fx_config.py` 中使用它：
```python
{"type": "custom", "name": "MyCustomEffect", "params": {"param1": 2.0}}
```

### 使用 VST3 插件

安裝 VST3 插件（選用）：
```bash
brew install surge-xt  # 免費的合成器和效果器套組
```

加入到你的效果鏈：
```python
{"type": "vst3", "path": "/Library/Audio/Plug-Ins/VST3/Surge XT.vst3"}
```

更多免費 VST3 插件：
- [Surge XT](https://surge-synthesizer.github.io/)
- [Vital](https://vital.audio/)
- [TAL Effects](https://tal-software.com/)

## 📂 專案結構

```
main.py              # 程式進入點 - 從這裡開始
audio_config.py      # 音訊裝置和效能設定
fx_config.py         # 在這裡定義你的效果鏈
fx_custom.py         # 撰寫自訂 Python 效果
audio_engine.py      # 即時音訊處理引擎
plugin_manager.py    # 效果載入系統
mod_aud_rec.py      # 錄音功能
output/             # 錄音檔案儲存位置
```

## 🎯 未來功能想法

來自社群的提案：
- **Looper**（循環器）- 錄製並循環播放吉他樂句（Jerry 的想法）
- **調性自動校正** - 將音符量化到特定音階（張永承的想法）
- MIDI 控制器支援
- 即時參數自動化
- 行動 App 介面

歡迎貢獻並加入這些功能！

## 🤔 技術說明

### 關於延遲

專業吉他效果器通常使用 C++ 搭配 JUCE 框架來達到超低延遲（<5ms）。這個 Python 實作目標是約 10ms 的延遲，對大多數演奏風格來說是可接受的。權衡如下：

- **Python 優點：** 容易編寫、快速原型開發、非常適合學習 DSP
- **Python 缺點：** 由於直譯式語言特性和垃圾回收機制，延遲比 C++ 高

對大多數演奏者來說，10ms 的延遲是無法察覺的。如果你需要更低的延遲，可以考慮使用專用硬體效果器或 C++ 實作。

### 效能調校技巧

- 在 `audio_config.py` 中降低 `BLOCK_SIZE` 可以獲得更低延遲（但會消耗更多 CPU）
- 保持效果鏈簡短（3-5 個效果）以獲得最佳效能
- 內建的 Pedalboard 效果（C++）比自訂 Python 效果更快
- 關閉其他音訊應用程式以減少系統負載

## 📚 參考資源

- [Spotify Pedalboard 文件](https://spotify.github.io/pedalboard/)
- [Python 音訊程式設計](https://realpython.com/playing-and-recording-sound-python/)
- [數位訊號處理基礎](https://jackschaedler.github.io/circles-sines-signals/)

## 🤝 參與貢獻

這個專案非常適合 vibe coding！無論你是資深工程師還是剛入門：

1. Fork 這個專案
2. 創建新的效果或功能
3. 用你的吉他測試它
4. 提交 pull request

沒有貢獻是太小的 - bug 修復、文件改善和新效果都非常歡迎！

## 📝 授權條款

本專案採用 [GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.en.html)。

---

**盡情享受音樂創作！🎵**
