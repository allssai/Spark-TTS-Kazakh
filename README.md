# Kazakh Spark-TTS Tool

Fine-tuned Spark-TTS for Kazakh text-to-speech with voice cloning, supporting Cyrillic and Tote Zhazu (Arabic) scripts.

### Key Features

- 🎯 **High-Quality Kazakh TTS**: Natural and fluent speech synthesis
- 🎤 **Voice Cloning**: Clone any voice with 3-10 seconds of reference audio
- 📝 **Dual Script Support**: Cyrillic and Tote Zhazu scripts
- ⚡ **Fast Inference**: Optimized for real-time generation

The GitHub repository includes:
- ✅ FastAPI REST API server
- ✅ Web-based user interface
- ✅ Complete documentation and examples
- ✅ Easy installation and deployment
  

![image](https://cdn-uploads.huggingface.co/production/uploads/6734991221f050f3604c7afd/jd-d6yM5raOnorh8AuGH3.png)



## Quick start

```bash
# Clone repository
git clone https://github.com/allssai/Spark-TTS-Kazakh.git
cd Spark-TTS-Kazakh

# Model weights
Hugging Face: `ErnarBahat/Spark-TTS-Kazakh`

```bash
huggingface-cli download ErnarBahat/Spark-TTS-Kazakh --local-dir ./pretrained_models/Kazakh-Spark-Final

# or
git lfs install
git clone https://huggingface.co/ErnarBahat/Spark-TTS-Kazakh pretrained_models/Kazakh-Spark-Final

# Install dependencies
pip install -r requirement.txt

# Run application
python app.py
```

Server: `http://localhost:8002`

## Usage

### REST API

```python
import requests

# Text-to-speech
requests.post("http://localhost:8002/tts", json={"text": "Сәлеметсіз бе!", "script": "cyrillic"})

# Voice cloning
files = {"audio": open("reference.wav", "rb")}
data = {"text": "Сәлеметсіз бе!"}
requests.post("http://localhost:8002/clone", files=files, data=data)
```

### CLI

```bash
python infer.py --text "Сәлеметсіз бе!" --output output.wav
python infer.py --text "Сәлеметсіз бе!" --reference voice.wav --output cloned.wav
```

## Project structure

```text
├── app.py                 # FastAPI server
├── infer.py              # Inference script
├── cli/                  # SparkTTS core modules
├── sparktts/             # SparkTTS library
├── static/               # Web UI
├── src/                  # Source code
├── config_axolotl/       # Training configs
├── example/              # Example files
└── examples/             # Code examples
```

## License

Apache License 2.0 — see [LICENSE](LICENSE).

## Citation

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
