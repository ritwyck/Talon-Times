import os
import torch
import whisper
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

# === Configure external drive caching directory for all models and tokenizers ===
# Change to your external drive path
external_cache_dir = "/Volumes/Gufa/models_cache"
os.makedirs(external_cache_dir, exist_ok=True)

# Set environment variables so Hugging Face and Whisper use this cache dir
os.environ["TRANSFORMERS_CACHE"] = external_cache_dir
os.environ["HF_HOME"] = external_cache_dir
os.environ["HF_DATASETS_CACHE"] = external_cache_dir
os.environ["HF_METRICS_CACHE"] = external_cache_dir
os.environ["XDG_CACHE_HOME"] = external_cache_dir

# === Detect device once ===
device = "cuda" if torch.cuda.is_available() else "cpu"

# === Load Whisper model once and reuse ===
_whisper_model = None


def load_whisper(model_name="large-v2"):
    global _whisper_model
    if _whisper_model is None:
        _whisper_model = whisper.load_model(model_name, device=device)
    return _whisper_model


# === Load summarization pipeline once and reuse ===
_summarizer = None


def get_summarizer_pipeline(model_name="sshleifer/distilbart-cnn-12-6"):
    global _summarizer
    if _summarizer is None:
        cache_path = os.path.join(
            external_cache_dir, model_name.replace("/", "_"))
        if not os.path.exists(cache_path):
            # Download and cache the model and tokenizer
            tokenizer = AutoTokenizer.from_pretrained(model_name)
            model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
            tokenizer.save_pretrained(cache_path)
            model.save_pretrained(cache_path)
        else:
            tokenizer = AutoTokenizer.from_pretrained(cache_path)
            model = AutoModelForSeq2SeqLM.from_pretrained(cache_path)

        _summarizer = pipeline(
            "summarization",
            model=model,
            tokenizer=tokenizer,
            device=0 if device == "cuda" else -1
        )
    return _summarizer

# === Transcribe audio with Whisper model ===


def transcribe_audio(audio_path, whisper_model):
    result = whisper_model.transcribe(audio_path)
    return result["text"]

# === Summarize text with summarizer pipeline ===


def summarize_text_fn(text, summarizer_pipe, max_length=130, min_length=30):
    if len(text.split()) < min_length:
        return text
    summary = summarizer_pipe(
        text, max_length=max_length, min_length=min_length, do_sample=False)
    return summary[0]["summary_text"]
