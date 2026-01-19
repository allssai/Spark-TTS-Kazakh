"""
Kazakh Spark-TTS Voice Cloning Example

This script demonstrates voice cloning using a reference audio sample.
"""

import torch
import torchaudio
import soundfile as sf
from transformers import AutoModel

def main():
    # Load model
    print("Loading model...")
    model = AutoModel.from_pretrained("YOUR_USERNAME/kazakh-spark-tts")
    model.eval()
    
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = model.to(device)
    print(f"Model loaded on {device}")
    
    # Load reference audio
    reference_audio_path = "reference_voice.wav"
    reference_text = "Бұл үлгі аудио."  # Transcription of reference audio
    
    print(f"\nLoading reference audio: {reference_audio_path}")
    ref_audio, sr = torchaudio.load(reference_audio_path)
    
    # Resample if necessary
    if sr != 16000:
        resampler = torchaudio.transforms.Resample(sr, 16000)
        ref_audio = resampler(ref_audio)
    
    # Move to device
    ref_audio = ref_audio.to(device)
    
    # Text to synthesize with cloned voice
    target_texts = [
        "Сәлеметсіз бе!",
        "Бүгін ауа райы өте жақсы.",
        "Мен қазақша сөйлей аламын."
    ]
    
    # Generate speech with cloned voice
    for i, text in enumerate(target_texts):
        print(f"\nCloning voice for: {text}")
        
        with torch.no_grad():
            audio = model.generate(
                text=text,
                prompt_speech=ref_audio,
                prompt_text=reference_text,
                temperature=0.3,
                top_k=20,
                top_p=0.7,
                repetition_penalty=1.1
            )
        
        # Save audio file
        output_file = f"cloned_output_{i+1}.wav"
        sf.write(output_file, audio.cpu().numpy(), 16000)
        print(f"Saved to {output_file}")

if __name__ == "__main__":
    main()
