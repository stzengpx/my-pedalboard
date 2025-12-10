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
2. **Python 3.8+** - 檢查你的版本：
   ```bash
   python3 --version
   ```
   如果你還沒有 Python，可以透過 [Homebrew](https://brew.sh/) 安裝：
   ```bash
   brew install python3
   ```

3. **音訊介面**（建議）- 任何 USB 音訊介面都可以用來輸入吉他訊號
   - 例如：Focusrite Scarlett、Spark 2 或類似產品

### 推薦開發環境

我們推薦使用 **[Google Antigravity](https://antigravity.google)** 進行開發：
- AI 驅動的程式碼輔助
- 瀏覽器為基礎，不需要本地端設定
- 完美適合 vibe coding 和實驗
- 非常適合想專注於創意而非繁瑣設定的工程師

### 安裝步驟

1. **複製這個專案：**
   ```bash
   git clone <your-repo-url>
   cd 20251128-my-pedalboard
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

按下 `Enter` 停止 pedalboard。錄音檔案會儲存在 `output/` 目錄中。

## 🎛️ 內建效果器

以下效果無需額外插件即可使用：

### 吉他效果 & 調變
- **Chorus**（合唱）- 豐富的漩渦調變效果
- **Distortion**（破音）- Overdrive 和破音音色
- **Phaser**（相位器）- 經典的相位移動效果

### 動態處理
- **Compressor**（壓縮器）- 動態範圍控制
- **Gain**（增益）- 音量增減
- **Limiter**（限幅器）- 防止削波失真

### 等化器 & 濾波器
- **HighpassFilter**（高通濾波器）- 移除低頻
- **LowpassFilter**（低通濾波器）- 移除高頻
- **LadderFilter**（階梯濾波器）- Moog 風格的多模式濾波器

### 空間 & 時間效果
- **Delay**（延遲）- 回音效果
- **Reverb**（殘響）- 空間氛圍
- **Convolution**（迴旋）- 基於脈衝響應的音箱/空間模擬

### 音高 & 音色
- **PitchShift**（移調）- 改變音高而不影響速度

### Lo-fi & 音色特性
- **GSMFullRateCompressor** - 復古電話失真效果
- **MP3Compressor** - MP3 壓縮失真
- **Resample**（重新取樣）- Bit-crush 和降低取樣率

### 工具類
- **Mix**（混音）- 混合多個效果鏈

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
