# Release Notes

## [0.0.2] - 2025-12-12

### 1. CLI Preset Loading (快速切換預設效果)

現在你可以透過指令列參數 `-p` 快速載入預設的效果鏈配置！

**使用方式：**

```bash
# Loading Preset: Clean Tone (清甜音色)
python3 main.py -p a1

# Loading Preset: Lead Guitar (金屬主奏)
python3 main.py -p a2

# Loading Preset: Solo Guitar (唱功獨奏)
python3 main.py -p a3

# Loading Preset: Crunch (節奏伴奏)
python3 main.py -p a4
```

詳細說明請參考：[README.md#執行-pedalboard](./README.md#執行-pedalboard)

### 2. Modular Custom Effect Development (模組化自定義效果器)

我們將自定義效果器的開發模組化了！現在你可以更輕鬆地開發和分享你的效果器，而不會與其他人的程式碼產生衝突。

- 所有自定義效果器都放在 `fx_custom/` 目錄下。
- 只要新增遵循命名規則（`fx_*.py`）的檔案，系統就會自動載入。
- 支援多人同時開發不同的效果器檔案。

詳細開發指南請參考：[fx_custom/README.md](./fx_custom/README.md)

## [0.0.1] - 2025-12-11

### 1. 基本功能

- 基本的吉他效果器功能
- 支援 VST3 插件
- 支援自定義效果器

詳細請參考：[README.md](./README.md)