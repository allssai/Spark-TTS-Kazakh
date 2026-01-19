# Kazakh Spark-TTS Application

[English](#english) | [中文](#中文) | [Қазақша](#қазақша)

---

## English

### Overview

Production-ready application for Kazakh text-to-speech synthesis with voice cloning capabilities. Built on fine-tuned Spark-TTS model with REST API, web interface, and automatic script conversion.

### 🎯 Key Features

- ✅ **High-Quality TTS**: Natural-sounding Kazakh speech synthesis
- ✅ **Voice Cloning**: Clone any voice with 3-10 seconds of audio
- ✅ **Dual Script Support**: Automatic Cyrillic ↔ Tote Zhazu conversion
- ✅ **REST API**: Easy-to-use HTTP API with JSON responses
- ✅ **Web Interface**: User-friendly web UI
- ✅ **Production Ready**: Stable and optimized

### 📦 Model Weights

Download the fine-tuned model from Hugging Face:

👉 **[YOUR_USERNAME/kazakh-spark-tts](https://huggingface.co/YOUR_USERNAME/kazakh-spark-tts)**

### 🚀 Quick Start

#### Requirements

- Python 3.8+
- CUDA-capable GPU (4GB+ VRAM recommended)
- 8GB+ RAM

#### Installation

```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/kazakh-spark-tts.git
cd kazakh-spark-tts

# Install dependencies
pip install -r requirement.txt

# Download model from Hugging Face
pip install huggingface_hub
huggingface-cli download YOUR_USERNAME/kazakh-spark-tts --local-dir pretrained_models/Kazakh-Spark-Final
```

#### Run Server

```bash
python app.py
# Server runs at http://localhost:8002
# Browser will open automatically
```

### 📖 Usage

#### Web Interface

Open `http://localhost:8002` in your browser for the interactive UI.

#### REST API

**Basic TTS**

```bash
curl -X POST http://localhost:8002/api/tts \
  -F "text=Сәлеметсіз бе!" \
  -F "mode=direct"
```

**Voice Cloning**

```bash
curl -X POST http://localhost:8002/api/tts \
  -F "text=Бүгін ауа райы жақсы" \
  -F "prompt_text=Reference text" \
  -F "prompt_speech=@reference.mp3"
```

**Python Example**

```python
import requests

# Basic TTS
response = requests.post(
    "http://localhost:8002/api/tts",
    data={"text": "Сәлеметсіз бе!", "mode": "direct"}
)

# Voice Cloning
with open("reference.mp3", "rb") as f:
    response = requests.post(
        "http://localhost:8002/api/tts",
        data={
            "text": "Бүгін ауа райы жақсы",
            "prompt_text": "Reference transcription"
        },
        files={"prompt_speech": f}
    )
```

### 🔧 Features

#### Tote Zhazu-Cyrillic Conversion

Automatic conversion between Tote Zhazu and Cyrillic scripts with 93.3% accuracy (300+ word dictionary).

#### Voice Cloning

Clone any voice with 3-10 seconds of reference audio. Supports WAV, MP3, and FLAC formats.

### 📁 Project Structure

```
kazakh-spark-tts/
├── app.py                      # FastAPI server
├── arab2cyr.py                 # Tote Zhazu→Cyrillic converter
├── cyr2arab.py                 # Cyrillic→Tote Zhazu converter
├── cli/SparkTTS.py            # Core TTS engine
├── sparktts/                  # Model utilities
├── static/                    # Web UI
└── pretrained_models/         # Model weights (download separately)
```

### 📚 Documentation

- [Quick Start Guide](QUICK_START.md) - Get started quickly
- [Tote Zhazu Converter](ARAB2CYR_OPTIMIZATION.md) - Converter details
- [Fixes and Optimizations](FIXES_AND_OPTIMIZATIONS.md) - Technical improvements
- [Quick Reference](QUICK_REFERENCE.md) - Common tasks

### 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### 📄 License

Apache License 2.0 - see [LICENSE](LICENSE) for details.

### 🙏 Acknowledgments

- Based on [Spark-TTS](https://github.com/SparkAudio/Spark-TTS)
- Fine-tuned for Kazakh language
- Tote Zhazu-Cyrillic converter with 300+ word dictionary

---

## 中文

### 概述

哈萨克语文本转语音生产级应用，支持语音克隆功能。基于微调的 Spark-TTS 模型，提供 REST API、Web 界面和自动文字转换。

### 🎯 主要特性

- ✅ **高质量TTS**: 自然流畅的哈萨克语语音合成
- ✅ **语音克隆**: 使用3-10秒音频克隆任意声音
- ✅ **双文字支持**: 西里尔字母 ↔ Tote Zhazu 自动转换
- ✅ **REST API**: 易用的HTTP API，JSON响应
- ✅ **Web界面**: 用户友好的界面
- ✅ **生产就绪**: 稳定且优化

### 📦 模型权重

从 Hugging Face 下载微调模型：

👉 **[YOUR_USERNAME/kazakh-spark-tts](https://huggingface.co/YOUR_USERNAME/kazakh-spark-tts)**

### 🚀 快速开始

#### 系统要求

- Python 3.8+
- 支持CUDA的GPU（推荐4GB+显存）
- 8GB+内存

#### 安装

```bash
# 克隆仓库
git clone https://github.com/YOUR_USERNAME/kazakh-spark-tts.git
cd kazakh-spark-tts

# 安装依赖
pip install -r requirement.txt

# 从 Hugging Face 下载模型
pip install huggingface_hub
huggingface-cli download YOUR_USERNAME/kazakh-spark-tts --local-dir pretrained_models/Kazakh-Spark-Final
```

#### 启动服务器

```bash
python app.py
# 服务器运行在 http://localhost:8002
# 浏览器会自动打开
```

### 📖 使用方法

#### Web界面

在浏览器中打开 `http://localhost:8002` 使用交互式界面。

#### REST API

**基本TTS**

```bash
curl -X POST http://localhost:8002/api/tts \
  -F "text=Сәлеметсіз бе!" \
  -F "mode=direct"
```

**语音克隆**

```bash
curl -X POST http://localhost:8002/api/tts \
  -F "text=Бүгін ауа райы жақсы" \
  -F "prompt_text=参考文本" \
  -F "prompt_speech=@reference.mp3"
```

**Python 示例**

```python
import requests

# 基本TTS
response = requests.post(
    "http://localhost:8002/api/tts",
    data={"text": "Сәлеметсіз бе!", "mode": "direct"}
)

# 语音克隆
with open("reference.mp3", "rb") as f:
    response = requests.post(
        "http://localhost:8002/api/tts",
        data={
            "text": "Бүгін ауа райы жақсы",
            "prompt_text": "参考音频转录"
        },
        files={"prompt_speech": f}
    )
```

### 🔧 功能特性

#### Tote Zhazu-西里尔文转换

自动在 Tote Zhazu 和西里尔文之间转换，准确率 93.3%（300+词词典）。

#### 语音克隆

使用 3-10 秒参考音频克隆任意声音。支持 WAV、MP3 和 FLAC 格式。

### 📁 项目结构

```
kazakh-spark-tts/
├── app.py                      # FastAPI 服务器
├── arab2cyr.py                 # Tote Zhazu→西里尔文转换器
├── cyr2arab.py                 # 西里尔文→Tote Zhazu 转换器
├── cli/SparkTTS.py            # 核心 TTS 引擎
├── sparktts/                  # 模型工具
├── static/                    # Web 界面
└── pretrained_models/         # 模型权重（单独下载）
```

### 📚 文档

- [快速开始指南](QUICK_START.md) - 快速入门
- [Tote Zhazu 转换器](ARAB2CYR_OPTIMIZATION.md) - 转换器详情
- [修复和优化](FIXES_AND_OPTIMIZATIONS.md) - 技术改进
- [快速参考](QUICK_REFERENCE.md) - 常见任务

### 🤝 贡献

欢迎贡献！请阅读 [CONTRIBUTING.md](CONTRIBUTING.md) 了解指南。

### 📄 许可证

Apache License 2.0 - 详见 [LICENSE](LICENSE) 文件。

### 🙏 致谢

- 基于 [Spark-TTS](https://github.com/SparkAudio/Spark-TTS)
- 为哈萨克语微调
- Tote Zhazu-西里尔文转换器（300+词词典）

---

## Қазақша

### Шолу

Қазақ тілі үшін дауысты клондау мүмкіндігімен өндірістік дайын мәтіннен сөйлеуге түрлендіру қосымшасы. REST API, веб-интерфейс және автоматты жазу түрлендіруімен жетілдірілген Spark-TTS моделіне негізделген.

### 🎯 Негізгі мүмкіндіктер

- ✅ **Жоғары сапалы TTS**: Табиғи қазақ тілінде сөйлеу синтезі
- ✅ **Дауысты клондау**: 3-10 секундтық аудиомен кез келген дауысты клондау
- ✅ **Екі жазу жүйесі**: Кирилл ↔ Төте жазу автоматты түрлендіру
- ✅ **REST API**: Пайдалануға оңай HTTP API
- ✅ **Веб-интерфейс**: Пайдаланушыға ыңғайлы интерфейс
- ✅ **Өндіріске дайын**: Тұрақты және оңтайландырылған

### 📦 Модель салмақтары

Hugging Face-тен жетілдірілген модельді жүктеп алыңыз:

👉 **[YOUR_USERNAME/kazakh-spark-tts](https://huggingface.co/YOUR_USERNAME/kazakh-spark-tts)**

### 🚀 Жылдам бастау

#### Жүйе талаптары

- Python 3.8+
- CUDA қолдайтын GPU (4GB+ VRAM ұсынылады)
- 8GB+ RAM

#### Орнату

```bash
# Репозиторийді клондау
git clone https://github.com/YOUR_USERNAME/kazakh-spark-tts.git
cd kazakh-spark-tts

# Тәуелділіктерді орнату
pip install -r requirement.txt

# Hugging Face-тен модельді жүктеу
pip install huggingface_hub
huggingface-cli download YOUR_USERNAME/kazakh-spark-tts --local-dir pretrained_models/Kazakh-Spark-Final
```

#### Серверді іске қосу

```bash
python app.py
# Сервер http://localhost:8002 мекенжайында жұмыс істейді
# Браузер автоматты түрде ашылады
```

### 📖 Пайдалану

#### Веб-интерфейс

Интерактивті интерфейс үшін браузерде `http://localhost:8002` ашыңыз.

#### REST API

**Негізгі TTS**

```bash
curl -X POST http://localhost:8002/api/tts \
  -F "text=Сәлеметсіз бе!" \
  -F "mode=direct"
```

**Дауысты клондау**

```bash
curl -X POST http://localhost:8002/api/tts \
  -F "text=Бүгін ауа райы жақсы" \
  -F "prompt_text=Анықтама мәтіні" \
  -F "prompt_speech=@reference.mp3"
```

**Python мысалы**

```python
import requests

# Негізгі TTS
response = requests.post(
    "http://localhost:8002/api/tts",
    data={"text": "Сәлеметсіз бе!", "mode": "direct"}
)

# Дауысты клондау
with open("reference.mp3", "rb") as f:
    response = requests.post(
        "http://localhost:8002/api/tts",
        data={
            "text": "Бүгін ауа райы жақсы",
            "prompt_text": "Анықтама аудио транскрипциясы"
        },
        files={"prompt_speech": f}
    )
```

### 🔧 Мүмкіндіктер

#### Төте жазу-Кирилл түрлендіру

Төте жазу мен Кирилл арасында автоматты түрлендіру, дәлдік 93.3% (300+ сөз сөздігі).

#### Дауысты клондау

3-10 секундтық анықтама аудиомен кез келген дауысты клондау. WAV, MP3 және FLAC форматтарын қолдайды.

### 📁 Жоба құрылымы

```
kazakh-spark-tts/
├── app.py                      # FastAPI сервері
├── arab2cyr.py                 # Төте жазу→Кирилл түрлендіргіші
├── cyr2arab.py                 # Кирилл→Төте жазу түрлендіргіші
├── cli/SparkTTS.py            # Негізгі TTS қозғалтқышы
├── sparktts/                  # Модель утилиталары
├── static/                    # Веб-интерфейс
└── pretrained_models/         # Модель салмақтары (бөлек жүктеу)
```

### 📚 Құжаттама

- [Жылдам бастау нұсқаулығы](QUICK_START.md) - Жылдам бастау
- [Төте жазу түрлендіргіші](ARAB2CYR_OPTIMIZATION.md) - Түрлендіргіш мәліметтері
- [Түзетулер және оңтайландырулар](FIXES_AND_OPTIMIZATIONS.md) - Техникалық жақсартулар
- [Жылдам анықтама](QUICK_REFERENCE.md) - Жалпы тапсырмалар

### 🤝 Үлес қосу

Үлес қосуға қош келдіңіз! Нұсқаулықтар үшін [CONTRIBUTING.md](CONTRIBUTING.md) оқыңыз.

### 📄 Лицензия

Apache License 2.0 - толық ақпарат үшін [LICENSE](LICENSE) файлын қараңыз.

### 🙏 Алғыс

- [Spark-TTS](https://github.com/SparkAudio/Spark-TTS) негізінде
- Қазақ тілі үшін жетілдірілген
- Төте жазу-Кирилл түрлендіргіші (300+ сөз сөздігі)

---

## 📞 Contact

- **Model**: [Hugging Face](https://huggingface.co/YOUR_USERNAME/kazakh-spark-tts)
- **Code**: [GitHub](https://github.com/YOUR_USERNAME/kazakh-spark-tts)
- **Issues**: [GitHub Issues](https://github.com/YOUR_USERNAME/kazakh-spark-tts/issues)

---

**Version**: 1.0.0  
**Last Updated**: 2026-01-19  
**Status**: 🟢 Production Ready
