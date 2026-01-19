import os
import re
import uuid
import torch
import numpy as np
import soundfile as sf
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional, List
from pathlib import Path
from datetime import datetime
import logging
import asyncio
from fastapi.concurrency import run_in_threadpool

# Import SparkTTS from the cli directory
from cli.SparkTTS import SparkTTS
from arab2cyr import ArabicToCyrillicConverter

# Initialize Converter
arabic_converter = ArabicToCyrillicConverter()

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI(title="Kazakh-TTS-Spark API", description="API for Kazakh Text-to-Speech")

# Constants
MODEL_DIR = Path("pretrained_models/Kazakh-Spark-Final")
OUTPUT_DIR = Path("static/outputs")
TEMP_DIR = Path("temp")
DEFAULT_PROMPT_WAV = Path("example/3.mp3")
DEFAULT_PROMPT_TEXT = "Тіпті құстар да оның жанынан өткенде үнсіз қалатын."
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Ensure directories exist
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
TEMP_DIR.mkdir(parents=True, exist_ok=True)

# Initialize Model
logger.info(f"Initializing Spark-TTS model from {MODEL_DIR} on {DEVICE}...")
try:
    model = SparkTTS(MODEL_DIR, DEVICE)
    logger.info("Model initialized successfully.")
except Exception as e:
    logger.error(f"Failed to initialize model: {e}")
    # In a real environment, we might want to exit here, 
    # but for development we'll allow it to fail later if called.
    model = None

# Models
class TTSRequest(BaseModel):
    text: str
    mode: str = "direct"  # "direct" or "segmented"
    temperature: float = 0.3
    top_k: int = 20
    top_p: float = 0.7

def split_text(text: str, max_length: int = 80) -> List[str]:
    """
    Optimized text splitting logic for segmented inference.
    Tries splitting by hierarchy:
    1. Sentence boundaries (.!?\n)
    2. Phrase boundaries (,;:)
    3. Word boundaries (spaces)
    """
    # Normalize line breaks
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    
    # Step 1: Initial split by sentence boundaries
    segments = re.split(r'(?<=[.!?\n])\s*', text)
    
    refined_segments = []
    for seg in segments:
        seg = seg.strip()
        if not seg: continue
        
        if len(seg) <= max_length:
            refined_segments.append(seg)
        else:
            # Step 2: Split by phrase boundaries
            phrases = re.split(r'(?<=[,;:])\s*', seg)
            for phrase in phrases:
                phrase = phrase.strip()
                if not phrase: continue
                
                if len(phrase) <= max_length:
                    refined_segments.append(phrase)
                else:
                    # Step 3: Split by words
                    words = phrase.split(' ')
                    current_sub_chunk = ""
                    for word in words:
                        if not word: continue
                        if len(current_sub_chunk) + len(word) + 1 <= max_length:
                            current_sub_chunk = (current_sub_chunk + " " + word).strip()
                        else:
                            if current_sub_chunk:
                                refined_segments.append(current_sub_chunk)
                            current_sub_chunk = word
                    if current_sub_chunk:
                        refined_segments.append(current_sub_chunk)

    # Group segments into larger chunks up to max_length for efficiency
    chunks = []
    current_chunk = ""
    for seg in refined_segments:
        if len(current_chunk) + len(seg) + 1 <= max_length:
            current_chunk = (current_chunk + " " + seg).strip()
        else:
            if current_chunk:
                chunks.append(current_chunk)
            current_chunk = seg
    if current_chunk:
        chunks.append(current_chunk)
        
    return chunks

@app.post("/api/tts")
async def generate_tts(
    text: str = Form(...),
    mode: str = Form("direct"),
    script: str = Form("cyrillic"),  # "cyrillic" or "arabic"
    temperature: float = Form(0.3),
    top_k: int = Form(20),
    top_p: float = Form(0.7),
    prompt_speech: Optional[UploadFile] = File(None),
    prompt_text: Optional[str] = Form(None)
):
    if model is None:
        raise HTTPException(status_code=500, detail="Model not initialized")

    try:
        # Convert script if necessary
        original_text = text
        if script == "arabic":
            text = arabic_converter.convert(text)
            logger.info(f"Converted Arabic main text to Cyrillic: {text}")
            if prompt_text and prompt_text.strip():
                prompt_text = arabic_converter.convert(prompt_text)
                logger.info(f"Converted Arabic prompt text to Cyrillic: {prompt_text}")
        
        if prompt_speech:
            prompt_ext = prompt_speech.filename.split(".")[-1]
            prompt_path = TEMP_DIR / f"prompt_{uuid.uuid4()}.{prompt_ext}"
            with open(prompt_path, "wb") as f:
                f.write(await prompt_speech.read())
            # Voice cloning mode: Use provided prompt_text or None
            # If user provides prompt_text (audio transcription), use it for alignment
            # Otherwise use None and let the model work without text alignment
            if prompt_text and prompt_text.strip():
                current_prompt_text = prompt_text.strip()
                logger.info(f"Voice cloning mode: Using provided prompt_text: {current_prompt_text[:50]}...")
            else:
                current_prompt_text = None
                logger.info("Voice cloning mode: No prompt_text provided")
        else:
            # Direct generation mode: Use default prompt WITHOUT prompt_text
            # Setting prompt_text=None allows the model to use more semantic tokens
            # and generate complete content without text alignment constraints
            if DEFAULT_PROMPT_WAV.exists():
                prompt_path = DEFAULT_PROMPT_WAV
                current_prompt_text = None
                logger.info(f"Direct generation mode: Using default prompt without prompt_text")
            else:
                logger.warning("No prompt provided and default prompt not found!")
                prompt_path = None
                current_prompt_text = None

        filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}.wav"
        save_path = OUTPUT_DIR / filename

        if mode == "segmented":
            chunks = split_text(text)
            logger.info(f"Segmented mode: Split into {len(chunks)} chunks")
            all_wavs = []
            
            for i, chunk in enumerate(chunks):
                logger.info(f"Synthesizing chunk {i+1}/{len(chunks)}: {chunk[:30]}...")
                # Run inference in a threadpool to avoid blocking the event loop
                wav = await run_in_threadpool(
                    model.inference,
                    text=chunk,
                    prompt_speech_path=prompt_path,
                    prompt_text=current_prompt_text,
                    temperature=temperature,
                    top_k=top_k,
                    top_p=top_p
                )
                
                # Fix: Handle both torch.Tensor and numpy.ndarray
                if torch.is_tensor(wav):
                    wav_data = wav.cpu().numpy().squeeze()
                else:
                    wav_data = np.array(wav).squeeze()
                
                all_wavs.append(wav_data)
                logger.info(f"Chunk {i+1} completed.")
            
            # Reconstruct
            combined_wav = np.concatenate(all_wavs)
            sf.write(save_path, combined_wav, samplerate=16000)
        else:
            # Direct mode
            logger.info("Direct mode: Starting inference...")
            wav = await run_in_threadpool(
                model.inference,
                text=text,
                prompt_speech_path=prompt_path,
                prompt_text=current_prompt_text,
                temperature=temperature,
                top_k=top_k,
                top_p=top_p
            )
            
            # Fix: Handle both torch.Tensor and numpy.ndarray
            if torch.is_tensor(wav):
                wav_data = wav.cpu().numpy().squeeze()
            else:
                wav_data = np.array(wav).squeeze()
                
            sf.write(save_path, wav_data, samplerate=16000)
            logger.info("Direct inference completed.")

        # Cleanup prompt if it was a temp file
        if prompt_path and str(prompt_path).startswith(str(TEMP_DIR)):
            os.remove(prompt_path)

        return {
            "success": True, 
            "audio_url": f"/outputs/{filename}",
            "filename": filename,
            "original_text": original_text,
            "converted_text": text
        }

    except Exception as e:
        logger.error(f"Inference error: {e}")
        # Return a JSONResponse instead of raising HTTPException to avoid 
        # potentially breaking the connection in some environments
        return JSONResponse(
            status_code=500,
            content={"success": False, "detail": str(e)}
        )

@app.get("/api/health")
async def health_check():
    return {"status": "ok", "model_loaded": model is not None}

# Serve static files
app.mount("/outputs", StaticFiles(directory=str(OUTPUT_DIR)), name="outputs")
app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    import webbrowser
    import threading
    
    # 延迟打开浏览器，等待服务器启动
    def open_browser():
        import time
        time.sleep(2)  # 等待2秒让服务器启动
        webbrowser.open("http://localhost:8002")
    
    # 在后台线程中打开浏览器
    threading.Thread(target=open_browser, daemon=True).start()
    
    print("\n" + "="*50)
    print("🚀 Kazakh Spark-TTS Server Starting...")
    print("="*50)
    print(f"📍 Server URL: http://localhost:8002")
    print(f"📍 API Docs: http://localhost:8002/docs")
    print("🌐 Browser will open automatically...")
    print("="*50 + "\n")
    
    uvicorn.run(app, host="0.0.0.0", port=8002)
