# Spark-TTS-Kazakh

[English](#english) | [中文](#中文) | [Қазақша](#қазақша)

---

<a name="english"></a>
## 🎯 English

### Overview

**Spark-TTS-Kazakh** is a fine-tuned text-to-speech (TTS) model specifically optimized for the Kazakh language. Built on the Spark-TTS architecture, it provides high-quality speech synthesis with voice cloning capabilities, supporting both Cyrillic and Tote Zhazu (Arabic) scripts.

### Key Features

- 🎤 **Voice Cloning**: Clone any voice with just 3-10 seconds of reference audio
- 📝 **Dual Script Support**: Supports both Cyrillic and Tote Zhazu scripts
- 🌐 **REST API**: FastAPI-based server for easy integration
- 💻 **Web Interface**: User-friendly web UI for testing and demos
- ⚡ **Fast Inference**: Optimized for real-time generation

### Model Weights

Download the fine-tuned model from Hugging Face:

```bash
# Using huggingface-cli
huggingface-cli download ErnarBahat/Spark-TTS-Kazakh --local-dir ./pretrained_models/Kazakh-Spark-Final

# Or using git
git lfs install
git clone https://huggingface.co/ErnarBahat/Spark-TTS-Kazakh pretrained_models/Kazakh-Spark-Final
```

### Quick Start

#### Installation

```bash
# Clone repository
git clone https://github.com/allssai/Spark-TTS-Kazakh.git
cd Spark-TTS-Kazakh

# Install dependencies
pip install -r requirement.txt

# Download model weights (see above)
```

#### Run Application

```bash
# Start the server
python app.py

# Server will start at http://localhost:8002
# Browser will open automatically
```

### Usage

#### Web Interface

1. Open http://localhost:8002 in your browser
2. Enter Kazakh text (Cyrillic or Tote Zhazu)
3. (Optional) Upload reference audio for voice cloning
4. Click "Generate Speech"
5. Download the generated audio

#### REST API

```python
import requests

# Text-to-Speech
response = requests.post('http://localhost:8002/tts', json={
    'text': 'Сәлеметсіз бе!',
    'script': 'cyrillic'
})

# Voice Cloning
files = {'audio': open('reference.wav', 'rb')}
data = {'text': 'Сәлеметсіз бе!'}
response = requests.post('http://localhost:8002/clone', files=files, data=data)
```

#### Command Line

```bash
# Basic TTS
python infer.py --text "Сәлеметсіз бе!" --output output.wav

# Voice cloning
python infer.py --text "Сәлеметсіз бе!" --reference voice.wav --output cloned.wav
```

### Features

#### Voice Cloning

- Requires 3-10 seconds of reference audio
- Supports WAV, MP3, and other common formats
- Maintains voice characteristics and speaking style
- Works with both male and female voices

### Project Structure

```
Spark-TTS-Kazakh/
├── app.py                 # FastAPI server
├── infer.py              # Inference script
├── cli/                  # SparkTTS core modules
├── sparktts/             # SparkTTS library
├── static/               # Web interface
├── src/                  # Source code
├── config_axolotl/       # Training configs
├── example/              # Example files
└── examples/             # Code examples
```

### Documentation

- [Quick Start Guide](QUICK_START.md) - Get started quickly
- [Quick Reference](QUICK_REFERENCE.md) - Common commands and usage
- [Contributing Guide](CONTRIBUTING.md) - How to contribute
- [Changelog](CHANGELOG.md) - Version history
- [Model Files](MODEL_FILES_REQUIRED.md) - Required model files

### License

Apache License 2.0 - See [LICENSE](LICENSE) for details.

### Citation

```bibtex
@misc{kazakh_spark_tts_2026,
  title={Spark-TTS-Kazakh: Fine-tuned Kazakh Text-to-Speech Model},
  author={Ernar Bahat},
  year={2026},
  publisher={GitHub},
  howpublished={\url{https://github.com/allssai/Spark-TTS-Kazakh}},
  note={Model: \url{https://huggingface.co/ErnarBahat/Spark-TTS-Kazakh}}
}
```

### Acknowledgments

- Based on [Spark-TTS](https://github.com/SparkAudio/Spark-TTS)
- Trained on high-quality Kazakh speech data
- Community contributions and feedback

---

<a name="中文"></a>
## 🎯 中文

### 概述

**Spark-TTS-Kazakh** 是专门为哈萨克语优化的文本转语音（TTS）模型。基于 Spark-TTS 架构构建，提供高质量的语音合成和语音克隆功能，支持西里尔文和 Tote Zhazu（阿拉伯文）两种文字。

### 主要特性

- 🎤 **语音克隆**：仅需 3-10 秒参考音频即可克隆任何声音
- 📝 **双文字支持**：支持西里尔文和 Tote Zhazu 文字
- 🌐 **REST API**：基于 FastAPI 的服务器，易于集成
- 💻 **Web 界面**：用户友好的网页界面，便于测试和演示
- ⚡ **快速推理**：针对实时生成进行优化

### 模型权重

从 Hugging Face 下载微调后的模型：

```bash
# 使用 huggingface-cli
huggingface-cli download ErnarBahat/Spark-TTS-Kazakh --local-dir ./pretrained_models/Kazakh-Spark-Final

# 或使用 git
git lfs install
git clone https://huggingface.co/ErnarBahat/Spark-TTS-Kazakh pretrained_models/Kazakh-Spark-Final
```

### 快速开始

#### 安装

```bash
# 克隆仓库
git clone https://github.com/allssai/Spark-TTS-Kazakh.git
cd Spark-TTS-Kazakh

# 安装依赖
pip install -r requirement.txt

# 下载模型权重（见上文）
```

#### 运行应用

```bash
# 启动服务器
python app.py

# 服务器将在 http://localhost:8002 启动
# 浏览器将自动打开
```

### 使用方法

#### Web 界面

1. 在浏览器中打开 http://localhost:8002
2. 输入哈萨克语文本（西里尔文或 Tote Zhazu）
3. （可选）上传参考音频进行语音克隆
4. 点击"生成语音"
5. 下载生成的音频

#### REST API

```python
import requests

# 文本转语音
response = requests.post('http://localhost:8002/tts', json={
    'text': 'Сәлеметсіз бе!',
    'script': 'cyrillic'
})

# 语音克隆
files = {'audio': open('reference.wav', 'rb')}
data = {'text': 'Сәлеметсіз бе!'}
response = requests.post('http://localhost:8002/clone', files=files, data=data)
```

#### 命令行

```bash
# 基础 TTS
python infer.py --text "Сәлеметсіз бе!" --output output.wav

# 语音克隆
python infer.py --text "Сәлеметсіз бе!" --reference voice.wav --output cloned.wav
```

### 功能特性

#### 语音克隆

- 需要 3-10 秒参考音频
- 支持 WAV、MP3 和其他常见格式
- 保持声音特征和说话风格
- 适用于男声和女声

### 项目结构

```
Spark-TTS-Kazakh/
├── app.py                 # FastAPI 服务器
├── infer.py              # 推理脚本
├── cli/                  # SparkTTS 核心模块
├── sparktts/             # SparkTTS 库
├── static/               # Web 界面
├── src/                  # 源代码
├── config_axolotl/       # 训练配置
├── example/              # 示例文件
└── examples/             # 代码示例
```

### 文档

- [快速开始指南](QUICK_START.md) - 快速入门
- [快速参考](QUICK_REFERENCE.md) - 常用命令和用法
- [贡献指南](CONTRIBUTING.md) - 如何贡献
- [更新日志](CHANGELOG.md) - 版本历史
- [模型文件](MODEL_FILES_REQUIRED.md) - 所需模型文件

### 许可证

Apache License 2.0 - 详见 [LICENSE](LICENSE)

### 引用

```bibtex
@misc{kazakh_spark_tts_2026,
  title={Spark-TTS-Kazakh: Fine-tuned Kazakh Text-to-Speech Model},
  author={Ernar Bahat},
  year={2026},
  publisher={GitHub},
  howpublished={\url{https://github.com/allssai/Spark-TTS-Kazakh}},
  note={Model: \url{https://huggingface.co/ErnarBahat/Spark-TTS-Kazakh}}
}
```

### 致谢

- 基于 [Spark-TTS](https://github.com/SparkAudio/Spark-TTS)
- 使用高质量哈萨克语语音数据训练
- 社区贡献和反馈

---

<a name="қазақша"></a>
## 🎯 Қазақша

### Шолу

**Spark-TTS-Kazakh** - қазақ тіліне арнайы оңтайландырылған мәтіннен сөйлеуге (TTS) айналдыру моделі. Spark-TTS архитектурасына негізделген, жоғары сапалы сөйлеу синтезін және дауысты клондауды қамтамасыз етеді, кириллица және Төте жазу жазуларын қолдайды.

### Негізгі мүмкіндіктер

- 🎤 **Дауысты клондау**: Тек 3-10 секунд анықтама аудиосымен кез келген дауысты клондау
- 📝 **Екі жазу қолдауы**: Кириллица және Төте жазу қолдайды
- 🌐 **REST API**: Оңай интеграциялау үшін FastAPI негізіндегі сервер
- 💻 **Web интерфейсі**: Тестілеу және демонстрация үшін пайдаланушыға ыңғайлы веб-интерфейс
- ⚡ **Жылдам қорытынды**: Нақты уақытта генерациялау үшін оңтайландырылған

### Модель салмақтары

Hugging Face-тен реттелген модельді жүктеп алыңыз:

```bash
# huggingface-cli пайдалану
huggingface-cli download ErnarBahat/Spark-TTS-Kazakh --local-dir ./pretrained_models/Kazakh-Spark-Final

# Немесе git пайдалану
git lfs install
git clone https://huggingface.co/ErnarBahat/Spark-TTS-Kazakh pretrained_models/Kazakh-Spark-Final
```

### Жылдам бастау

#### Орнату

```bash
# Репозиторийді клондау
git clone https://github.com/allssai/Spark-TTS-Kazakh.git
cd Spark-TTS-Kazakh

# Тәуелділіктерді орнату
pip install -r requirement.txt

# Модель салмақтарын жүктеу (жоғарыда қараңыз)
```

#### Қолданбаны іске қосу

```bash
# Серверді іске қосу
python app.py

# Сервер http://localhost:8002 мекенжайында іске қосылады
# Браузер автоматты түрде ашылады
```

### Пайдалану

#### Web интерфейсі

1. Браузерде http://localhost:8002 ашыңыз
2. Қазақ тіліндегі мәтінді енгізіңіз (кириллица немесе Төте жазу)
3. (Қосымша) Дауысты клондау үшін анықтама аудиосын жүктеңіз
4. "Сөйлеу генерациялау" батырмасын басыңыз
5. Генерацияланған аудионы жүктеп алыңыз

#### REST API

```python
import requests

# Мәтіннен сөйлеуге
response = requests.post('http://localhost:8002/tts', json={
    'text': 'Сәлеметсіз бе!',
    'script': 'cyrillic'
})

# Дауысты клондау
files = {'audio': open('reference.wav', 'rb')}
data = {'text': 'Сәлеметсіз бе!'}
response = requests.post('http://localhost:8002/clone', files=files, data=data)
```

#### Командалық жол

```bash
# Негізгі TTS
python infer.py --text "Сәлеметсіз бе!" --output output.wav

# Дауысты клондау
python infer.py --text "Сәлеметсіз бе!" --reference voice.wav --output cloned.wav
```

### Мүмкіндіктер

#### Дауысты клондау

- 3-10 секунд анықтама аудиосы қажет
- WAV, MP3 және басқа жалпы форматтарды қолдайды
- Дауыс сипаттамаларын және сөйлеу стилін сақтайды
- Ер адам және әйел дауыстарымен жұмыс істейді

### Жоба құрылымы

```
Spark-TTS-Kazakh/
├── app.py                 # FastAPI сервері
├── infer.py              # Қорытынды скрипті
├── cli/                  # SparkTTS негізгі модульдері
├── sparktts/             # SparkTTS кітапханасы
├── static/               # Web интерфейсі
├── src/                  # Бастапқы код
├── config_axolotl/       # Оқыту конфигурациялары
├── example/              # Мысал файлдары
└── examples/             # Код мысалдары
```

### Құжаттама

- [Жылдам бастау нұсқаулығы](QUICK_START.md) - Жылдам бастау
- [Жылдам анықтама](QUICK_REFERENCE.md) - Жалпы пәрмендер мен пайдалану
- [Үлес қосу нұсқаулығы](CONTRIBUTING.md) - Қалай үлес қосу керек
- [Өзгерістер журналы](CHANGELOG.md) - Нұсқа тарихы
- [Модель файлдары](MODEL_FILES_REQUIRED.md) - Қажетті модель файлдары

### Лицензия

Apache License 2.0 - Толық ақпарат үшін [LICENSE](LICENSE) қараңыз

### Сілтеме

```bibtex
@misc{kazakh_spark_tts_2026,
  title={Spark-TTS-Kazakh: Fine-tuned Kazakh Text-to-Speech Model},
  author={Ernar Bahat},
  year={2026},
  publisher={GitHub},
  howpublished={\url{https://github.com/allssai/Spark-TTS-Kazakh}},
  note={Model: \url{https://huggingface.co/ErnarBahat/Spark-TTS-Kazakh}}
}
```

### Алғыс

- [Spark-TTS](https://github.com/SparkAudio/Spark-TTS) негізінде
- Жоғары сапалы қазақ сөйлеу деректерінде оқытылған
- Қоғамдастық үлестері мен кері байланыс

---

**Version**: 1.0.0 | **License**: Apache 2.0 | **Status**: Production Ready
