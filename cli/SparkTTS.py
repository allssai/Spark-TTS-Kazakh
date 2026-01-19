# Copyright (c) 2025 SparkAudio
#               2025 Xinsheng Wang (w.xinshawn@gmail.com)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import re
import torch
from typing import Tuple
from pathlib import Path
from transformers import AutoTokenizer, AutoModelForCausalLM
import os
import librosa
import numpy as np
import tempfile
import soundfile as sf

from sparktts.utils.file import load_config
from sparktts.models.audio_tokenizer import BiCodecTokenizer
from sparktts.utils.token_parser import LEVELS_MAP, GENDER_MAP, TASK_TOKEN_MAP


class SparkTTS:
    """
    Spark-TTS for text-to-speech generation.
    """

    def __init__(self, model_dir: Path, device: torch.device = torch.device("cuda:0")):
        """
        Initializes the SparkTTS model with the provided configurations and device.

        Args:
            model_dir (Path): Directory containing the model and config files.
            device (torch.device): The device (CPU/GPU) to run the model on.
        """
        self.device = device
        self.model_dir = model_dir
        self.configs = load_config(f"{model_dir}/config.yaml")
        self.sample_rate = self.configs["sample_rate"]
        self._initialize_inference()

    def _initialize_inference(self):
        """Initializes the tokenizer, model, and audio tokenizer for inference."""
        self.tokenizer = AutoTokenizer.from_pretrained(
            f"{self.model_dir}/LLM",
            use_fast=False,
            local_files_only=True,
            trust_remote_code=True
        )
        self.model = AutoModelForCausalLM.from_pretrained(
            f"{self.model_dir}/LLM",
            local_files_only=True,
            trust_remote_code=True
        )
        self.audio_tokenizer = BiCodecTokenizer(self.model_dir, device=self.device)
        self.model.to(self.device)

    def process_prompt(
        self,
        text: str,
        prompt_speech_path: Path,
        prompt_text: str = None,
    ) -> Tuple[str, torch.Tensor]:
        """
        Process input for voice cloning.

        Args:
            text (str): The text input to be converted to speech.
            prompt_speech_path (Path): Path to the audio file used as a prompt.
            prompt_text (str, optional): Transcript of the prompt audio.

        Return:
            Tuple[str, torch.Tensor]: Input prompt; global tokens
        """

        # Robust audio loading and normalization to 16kHz mono
        # This ensures compatibility with mp3 and prevents feature extraction issues
        wav, sr = librosa.load(str(prompt_speech_path), sr=16000, mono=True)
        
        # Use a temporary file to pass the normalized audio to the internal tokenizer
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
            temp_wav_path = f.name
            sf.write(temp_wav_path, wav, 16000)
            
        try:
            global_token_ids, semantic_token_ids = self.audio_tokenizer.tokenize(
                temp_wav_path
            )
        finally:
            if os.path.exists(temp_wav_path):
                os.remove(temp_wav_path)

        # CRITICAL: Standardize global tokens to exactly 32 frames for the instruction prompt
        # This prevents the prompt string from becoming excessively long (e.g., >6000 chars)
        g_ids_to_use = global_token_ids.squeeze()
        if g_ids_to_use.dim() == 0: g_ids_to_use = g_ids_to_use.unsqueeze(0)
        if g_ids_to_use.shape[0] != 32:
            indices = torch.linspace(0, g_ids_to_use.shape[0] - 1, 32).long()
            g_ids_to_use = g_ids_to_use[indices]
        
        global_tokens = "".join(
            [f"<|bicodec_global_{int(i)}|>" for i in g_ids_to_use]
        )
        
        # Prepare the input tokens for the model
        # CRITICAL FIX: Adaptive token count based on prompt_text presence
        # The total prompt length must stay under ~4000 chars to avoid model overflow
        
        # Ensure prompt_text is None if it's empty string
        if not prompt_text or not prompt_text.strip():
            prompt_text = None

        if prompt_text is not None:
            # Voice cloning with prompt_text: Include prompt_text in combined_text
            # This ensures proper alignment between semantic tokens and text
            # We'll trim the audio later to remove the prompt_text portion
            MAX_SEMANTIC_TOKENS = 80
            
            # Truncate semantic tokens to reasonable length
            s_ids_to_use = semantic_token_ids.squeeze()
            if s_ids_to_use.dim() == 0: s_ids_to_use = s_ids_to_use.unsqueeze(0)
            if s_ids_to_use.shape[0] > MAX_SEMANTIC_TOKENS:
                s_ids_to_use = s_ids_to_use[:MAX_SEMANTIC_TOKENS]
                
            semantic_tokens = "".join(
                [f"<|bicodec_semantic_{int(i)}|>" for i in s_ids_to_use]
            )
            
            # Truncate prompt_text if too long to keep prompt manageable
            if len(prompt_text) > 80:
                prompt_text = prompt_text[:80]
            
            # Include prompt_text in combined_text for proper alignment
            # The model will generate audio for both prompt_text and text
            combined_text = f" {prompt_text} {text}"
            
            # Store the prompt_text length for later audio trimming
            self.last_prompt_text_len = len(prompt_text)
            
            inputs = [
                TASK_TOKEN_MAP["tts"],
                "<|start_content|>",
                combined_text,
                "<|end_content|>",
                "<|start_global_token|>",
                global_tokens,
                "<|end_global_token|>",
                "<|start_semantic_token|>",
                semantic_tokens,
            ]
        else:
            # Without prompt_text: Don't use semantic tokens at all
            # Semantic tokens cause alignment issues and skip beginning
            # Global tokens alone are sufficient for voice cloning
            # This ensures the model generates from the very beginning
            
            # No semantic tokens
            semantic_tokens = ""
            
            # No prompt_text to trim
            self.last_prompt_text_len = 0
            
            # Use text directly without any prefix
            combined_text = f" {text}"
            inputs = [
                TASK_TOKEN_MAP["tts"],
                "<|start_content|>",
                combined_text,
                "<|end_content|>",
                "<|start_global_token|>",
                global_tokens,
                "<|end_global_token|>",
            ]

        inputs = "".join(inputs)

        # Return the standardized/truncated tokens and the input string
        # This ensures the detokenizer uses exactly what the model was conditioned on
        return inputs, g_ids_to_use

    def process_prompt_control(
        self,
        gender: str,
        pitch: str,
        speed: str,
        text: str,
    ):
        """
        Process input for voice creation.

        Args:
            gender (str): female | male.
            pitch (str): very_low | low | moderate | high | very_high
            speed (str): very_low | low | moderate | high | very_high
            text (str): The text input to be converted to speech.

        Return:
            str: Input prompt
        """
        assert gender in GENDER_MAP.keys()
        assert pitch in LEVELS_MAP.keys()
        assert speed in LEVELS_MAP.keys()

        gender_id = GENDER_MAP[gender]
        pitch_level_id = LEVELS_MAP[pitch]
        speed_level_id = LEVELS_MAP[speed]

        pitch_label_tokens = f"<|pitch_label_{pitch_level_id}|>"
        speed_label_tokens = f"<|speed_label_{speed_level_id}|>"
        gender_tokens = f"<|gender_{gender_id}|>"

        attribte_tokens = "".join(
            [gender_tokens, pitch_label_tokens, speed_label_tokens]
        )

        control_tts_inputs = [
            TASK_TOKEN_MAP["controllable_tts"],
            "<|start_content|>",
            text,
            "<|end_content|>",
            "<|start_style_label|>",
            attribte_tokens,
            "<|end_style_label|>",
        ]

        return "".join(control_tts_inputs)

    @torch.no_grad()
    def inference(
        self,
        text: str,
        prompt_speech_path: Path = None,
        prompt_text: str = None,
        gender: str = None,
        pitch: str = None,
        speed: str = None,
        temperature: float = 0.3,
        top_k: float = 20,
        top_p: float = 0.7,
    ) -> torch.Tensor:
        """
        Performs inference to generate speech from text, incorporating prompt audio and/or text.

        Args:
            text (str): The text input to be converted to speech.
            prompt_speech_path (Path): Path to the audio file used as a prompt.
            prompt_text (str, optional): Transcript of the prompt audio.
            gender (str): female | male.
            pitch (str): very_low | low | moderate | high | very_high
            speed (str): very_low | low | moderate | high | very_high
            temperature (float, optional): Sampling temperature for controlling randomness. Default is 0.8.
            top_k (float, optional): Top-k sampling parameter. Default is 50.
            top_p (float, optional): Top-p (nucleus) sampling parameter. Default is 0.95.

        Returns:
            torch.Tensor: Generated waveform as a tensor.
        """
        if gender is not None:
            prompt = self.process_prompt_control(gender, pitch, speed, text)

        else:
            prompt, global_token_ids = self.process_prompt(
                text, prompt_speech_path, prompt_text
            )
        model_inputs = self.tokenizer([prompt], return_tensors="pt").to(self.device)

        # Generate speech using the model
        # Added repetition_penalty=1.1 to prevent infinite generation loops (hallucinations)
        # Dynamic max_new_tokens based on text length for better quality and completeness
        # For Kazakh TTS: Each character needs ~15-20 semantic tokens on average
        # Plus additional tokens for formatting (<|bicodec_semantic_XXX|> tags)
        
        # CRITICAL: Calculate based on the actual text that will be generated
        # If prompt_text was included in combined_text, we need more tokens
        if hasattr(self, 'last_prompt_text_len') and self.last_prompt_text_len > 0:
            # Generate for both prompt_text and text
            total_text_len = self.last_prompt_text_len + len(text)
        else:
            # Generate only for text
            total_text_len = len(text)
        
        estimated_tokens = total_text_len * 15
        # Set minimum to 400 and maximum to 1500 (increased from 1200 for longer texts)
        max_new_tokens = min(max(estimated_tokens, 400), 1500)
        
        generated_ids = self.model.generate(
            **model_inputs,
            max_new_tokens=max_new_tokens,
            do_sample=True,
            top_k=top_k,
            top_p=top_p,
            temperature=temperature,
            repetition_penalty=1.1,
        )

        # Trim the output tokens to remove the input tokens
        generated_ids = [
            output_ids[len(input_ids) :]
            for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
        ]

        # Decode the generated tokens into text
        predicts = self.tokenizer.batch_decode(generated_ids, skip_special_tokens=False)[0]
        
        # DEBUG LOGGING
        with open("debug_output.txt", "a", encoding="utf-8") as f:
            f.write(f"\n--- Inference: {text} ---\n")
            f.write(f"PROMPT_USED: {prompt[:500]}... (Total len: {len(prompt)})\n")
            f.write(f"PREDICTS: {predicts}\n")
            f.write(f"TOTAL_PREDICT_LEN: {len(predicts)}\n")
            f.flush()
        
        # Extract semantic and global token IDs from the generated text
        semantic_matches = re.findall(r"bicodec_semantic_(\d+)", predicts)
        global_matches = re.findall(r"bicodec_global_(\d+)", predicts)
        
        if not semantic_matches:
            print(f"WARNING: No semantic tokens generated for: {text}")
            return torch.zeros(1, 1600).to(self.device)

        pred_semantic_ids = (
            torch.tensor([int(token) for token in semantic_matches])
            .long()
            .unsqueeze(0)
        )

        # Use generated global tokens if found, otherwise fallback to prompt global tokens
        if global_matches:
            global_token_ids = (
                torch.tensor([int(token) for token in global_matches])
                .long()
                .unsqueeze(0)
                .unsqueeze(0)
            )
        elif gender is not None:
            # For controllable mode, we MUST have global tokens
            print(f"WARNING: No global tokens generated for controllable TTS: {text}")
            return torch.zeros(1, 1600).to(self.device)
        # else: use the global_token_ids from process_prompt (cloning mode)

        # Convert semantic tokens back to waveform
        try:
            # Standardize s_ids to (1, N)
            s_ids = pred_semantic_ids.to(self.device).squeeze()
            if s_ids.dim() == 0: s_ids = s_ids.unsqueeze(0)
            s_ids = s_ids.unsqueeze(0) # (1, N)
            
            # Standardize g_ids to (1, 32)
            # Spark-TTS speaker encoder expects exactly 32 global tokens for the utterance style.
            # We resample the provided prompt global tokens to this fixed length.
            g_ids = global_token_ids.to(self.device).squeeze()
            if g_ids.dim() == 0: g_ids = g_ids.unsqueeze(0)
            
            if g_ids.shape[0] != 32:
                indices = torch.linspace(0, g_ids.shape[0] - 1, 32).long()
                g_ids = g_ids[indices]
            
            g_ids = g_ids.unsqueeze(0) # (1, 32)
            
            # Detokenize to generate final waveform
            wav = self.audio_tokenizer.detokenize(g_ids, s_ids)
            
            # CRITICAL: Trim prompt_text portion from the generated audio
            # If prompt_text was included in combined_text, we need to remove it
            if hasattr(self, 'last_prompt_text_len') and self.last_prompt_text_len > 0:
                # Estimate audio samples for prompt_text
                # Rough estimate: 1 character ≈ 0.08 seconds at 16kHz = 1280 samples
                # This is conservative to avoid cutting actual content
                samples_per_char = 1200  # Slightly less than 0.08s to be safe
                trim_samples = int(self.last_prompt_text_len * samples_per_char)
                
                # Ensure we don't trim more than 80% of the audio
                max_trim = int(wav.shape[-1] * 0.8)
                trim_samples = min(trim_samples, max_trim)
                
                if trim_samples > 0 and trim_samples < wav.shape[-1]:
                    wav = wav[..., trim_samples:]
                    with open("debug_output.txt", "a", encoding="utf-8") as f:
                        f.write(f"TRIMMED: {trim_samples} samples ({trim_samples/16000:.2f}s) for prompt_text length {self.last_prompt_text_len}\n")
                        f.flush()
                
                # Reset for next inference
                self.last_prompt_text_len = 0
                
        except Exception as e:
            print(f"Detokenization error: {e}")
            return torch.zeros(1, 1600).to(self.device)

        return wav
