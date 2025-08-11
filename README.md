# 🐾 Talon Times

**Sharp ears, sharper notes.**  
Talon Times is inspired by our puppy Talon — always alert, always listening, always ready to share what he heard.  
It captures your audio or text, transcribes it, summarises it, and saves it neatly as a PDF.  
You can even record right inside the app.

## ✨ Features
- 🎙 **Record Audio** — Capture conversations, meetings, or quick thoughts.
- 📝 **Transcribe** — Turn speech or raw text into clean, readable text.
- 📚 **Summarise** — Distill long content into bite-sized takeaways.
- 📄 **Save as PDF** — Organise your transcripts and summaries in one place.
- 💻 **Streamlit UI** — Friendly, interactive interface.
- 💾 **External Model Storage** — Backend models live on an external drive, keeping your main system uncluttered.

## 🛠 How It Works
1. You record or upload **audio**, or paste in **text**.
2. Backend model (stored on your external drive) **transcribes** speech to text.
3. A summariser condenses the text into essentials.
4. Everything is saved as a **PDF** for easy reference.
5. Repeat anytime — Talon’s always listening.

## 🚀 Getting Started
```bash
git clone https://github.com/ritwyck/Talon-Times.git
cd talon-times
pip install -r requirements.txt
streamlit run App.py
````

## 📂 Project Structure

```
Talon-Times/
│
├── App.py             # Streamlit UI
├── backend.py         # Audio recording
├── model_loader.py    # Speech-to-text engine

```

## ⚡ Requirements

* Python 3.10+
* Streamlit
* PyPDF2 / ReportLab
* SpeechRecognition / pyaudio
* Models stored on an **external drive** (mounted at `/models` or similar)

## 🐶 Why "Talon Times"?

Because like Talon, it’s attentive, quick to respond, and never misses the important bits.

```
