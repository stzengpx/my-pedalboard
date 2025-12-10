# My Pedalboard

## Dev Env
pip install -r requirements.txt

## Run
python main.py
python main.py -r

## Requirements
Jerry: 是不是可以寫成looper阿
張永承: 設定調性 讓彈錯也被調進調裡

## 預設內建的效果器

整理如下（指的是 from pedalboard import ... 直接用得到的那些 class）：​

- Guitar / 彩度類效果
    - Chorus
    - Distortion
    - Phaser
- 動態 / 音量相關
    - Compressor
    - Gain
    - Limiter
- EQ / 濾波
    - HighpassFilter
    - LowpassFilter
    - LadderFilter（Moog 風格的多模式濾波器）
- 空間 / 時間效果
    - Delay
    - Reverb
    - Convolution（載入 impulse response，模擬 amp / 空間）
- 音高 / 音色處理
    - PitchShift
- 品質 / 壓縮類
    - GSMFullRateCompressor（模擬 GSM 壓縮失真感）
    - MP3Compressor（模擬 MP3 壓縮）
    - Resample（降低取樣率做 lo‑fi / 變速等）
- 其他實用工具
    - Mix（把多條 Pedalboard / 軌一起混）

這些都是「不用裝額外 VST，就能直接 import 使用」的內建效果；
如果要更多效果，就要再載入外部 VST3 / AU plugin（例如 VST3Plugin 等）來用。

## Reference

- GitHub Repo: [spotify/pedalboard](https://github.com/spotify/pedalboard)
- 技術上的挑戰 延遲 Latency
    - 通常專業的吉他效果器是使用 "C++" 配合 JUCE 框架 開發的
    - 因為即時音訊處理需要極低的時間延遲 低於 10ms
        - Python 和 Node.js 雖然方便 但因為是直譯式語言Interpreted languages
        - 且有 Garbage Collection 機制，要做到「毫秒級」的即時運算會比較吃力
        - 可能會感覺到聲音稍微慢半拍。
- VST3 Plugin
    - brew install surge-xt
    - https://account.vital.audio