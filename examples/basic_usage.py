"""
Kazakh Spark-TTS Basic Usage Example

This script demonstrates basic text-to-speech generation using the Kazakh Spark-TTS model.
"""

import torch
import soundfile as sf
from transformers import AutoModel

def main():
    # Load model from Hugging Face
    print("Loading model...")
    model = AutoModel.from_pretrained("YOUR_USERNAME/kazakh-spark-tts")
    model.eval()
    
    # Move to GPU if available
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = model.to(device)
    print(f"Model loaded on {device}")
    
    # Example texts in Cyrillic
    texts = [
        "Сәлеметсіз бе!",
        "Бүгін ауа райы жақсы.",
        "Қазақстан - менің Отаным."
    ]
    
    # Generate speech for each text
    for i, text in enumerate(texts):
        print(f"\nGenerating speech for: {text}")
        
        with torch.no_grad():
            audio = model.generate(
                text=text,
                temperature=0.3,
                top_k=20,
                top_p=0.7,
                repetition_penalty=1.1
            )
        
        # Save audio file
        output_file = f"output_{i+1}.wav"
        sf.write(output_file, audio.cpu().numpy(), 16000)
        print(f"Saved to {output_file}")

if __name__ == "__main__":
    main()
