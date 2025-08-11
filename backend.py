from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import shutil, os

from model_loader import load_whisper, get_summarizer_pipeline, transcribe_audio, summarize_text_fn

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Insecure for production, fine for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

whisper_model = load_whisper()
summarizer_pipe = get_summarizer_pipeline()

class TextRequest(BaseModel):
    text: str

@app.post("/transcribe/")
async def transcribe_endpoint(file: UploadFile = File(...)):
    temp_file = f"temp_{file.filename}"
    with open(temp_file, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    transcript = transcribe_audio(temp_file, whisper_model)
    os.remove(temp_file)
    return {"transcript": transcript}

@app.post("/summarize/")
async def summarize_endpoint(request: TextRequest):
    summary = summarize_text_fn(request.text, summarizer_pipe)
    return {"summary": summary}

@app.post("/transcribe_and_summarize/")
async def transcribe_and_summarize_endpoint(file: UploadFile = File(...)):
    temp_file = f"temp_{file.filename}"
    with open(temp_file, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    transcript = transcribe_audio(temp_file, whisper_model)
    summary = summarize_text_fn(transcript, summarizer_pipe)
    os.remove(temp_file)
    return {"transcript": transcript, "summary": summary}
