# 🦅 Talon Times

**Catch every word. Keep every idea.**  
Talon Times is your personal listening bird of prey — it swoops down, grabs your audio/text, transcribes it, trims it into a summary, and tucks it safely into a PDF nest.  
Oh, and you can record right inside the app.  

## ✨ Features
- 🎙 **Record Audio** — Speak directly into the app.
- 📝 **Transcribe** — Convert audio or text input into clean, readable text.
- 📚 **Summarise** — Condense long rambles into sharp, digestible insights.
- 📄 **Save as PDF** — Neatly packaged transcripts & summaries for later.
- 💻 **Streamlit UI** — Lightweight, interactive, and friendly interface.
- 💾 **External Model Storage** — Models live on an external drive so your main machine stays lean.

## 🛠 How It Works
1. You feed it **audio** (recorded or uploaded) or raw **text**.
2. Backend model (on your external drive) **transcribes** speech to text.
3. A summariser model trims it down to the essentials.
4. Output is saved to a **PDF** file for safekeeping.
5. Repeat, and watch your knowledge archive grow.

## 🚀 Getting Started
```bash
git clone https://github.com/ritwyck/Talon-Times.git
cd talon-times
pip install -r requirements.txt
streamlit run App.py
