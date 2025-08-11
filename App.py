import streamlit as st
from model_loader import load_whisper, get_summarizer_pipeline, transcribe_audio, summarize_text_fn
from audiorecorder import audiorecorder
import tempfile
from datetime import datetime
from fpdf import FPDF
import os

# Cache models so they load only once


@st.cache_resource
def get_whisper():
    return load_whisper()


@st.cache_resource
def get_summarizer():
    return get_summarizer_pipeline()


# Load models once
whisper_model = load_whisper()
summarizer_pipe = get_summarizer_pipeline()

st.title("🎤 Transcription & Summarisation App")

mode = st.radio(
    "Select Mode",
    ["Transcribe", "Summarise", "Transcribe & Summarise"]
)


def save_text_to_pdf(text, filename):
    """Save given text to a PDF file and return path."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for line in text.split("\n"):
        pdf.multi_cell(0, 10, line)
    pdf.output(filename)
    return filename


if mode == "Just Summarisation":
    text_input = st.text_area("Enter text to summarise")
    if st.button("Submit"):
        if not text_input.strip():
            st.warning("Please enter some text to summarise")
        else:
            with st.spinner("Summarising… Please wait"):
                summary = summarize_text_fn(text_input, summarizer_pipe)
            st.success("Done!")
            st.subheader("Summary")
            st.write(summary)

            pdf_file = save_text_to_pdf(summary, "summary.pdf")
            with open(pdf_file, "rb") as f:
                st.download_button("📥 Download Summary as PDF",
                                   f, file_name="summary.pdf")

else:
    st.write("📁 Upload an audio file **or** record one below:")

    # Upload option
    audio_file = st.file_uploader("Upload audio", type=["wav", "mp3", "m4a"])

    # Record option
    recorded_audio = audiorecorder("🎙️ Click to record", "⏹️ Stop recording")

    if st.button("Submit"):
        audio_source = None
        save_audio_filename = f"audio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"

        if recorded_audio and len(recorded_audio) > 0:
            st.info("Using recorded audio")
            with open(save_audio_filename, "wb") as f:
                recorded_audio.export(f, format="wav")  # export as WAV format
            audio_source = save_audio_filename

            with open(save_audio_filename, "rb") as f:
                st.download_button("📥 Download Recorded Audio",
                                   f, file_name=save_audio_filename)

        elif audio_file:
            st.info("Using uploaded file")
            with open(save_audio_filename, "wb") as f:
                f.write(audio_file.getbuffer())
            audio_source = save_audio_filename

        if not audio_source:
            st.warning("Please upload or record an audio file")
            st.stop()

        with st.spinner("Processing audio… This may take a while"):
            transcript = transcribe_audio(audio_source, whisper_model)
            summary = None
            if mode == "Transcribe & Summarise":
                summary = summarize_text_fn(transcript, summarizer_pipe)

        st.success("Done!")

        st.subheader("Transcript")
        st.write(transcript)

        transcript_pdf = save_text_to_pdf(transcript, "transcript.pdf")
        with open(transcript_pdf, "rb") as f:
            st.download_button("📥 Download Transcript as PDF",
                               f, file_name="transcript.pdf")

        if summary:
            st.subheader("Summary")
            st.write(summary)
            summary_pdf = save_text_to_pdf(summary, "summary.pdf")
            with open(summary_pdf, "rb") as f:
                st.download_button("📥 Download Summary as PDF",
                                   f, file_name="summary.pdf")
