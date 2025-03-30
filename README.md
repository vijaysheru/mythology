

# 🕉️ MythOS: Talk to Lord Krishna — AI-Powered Spiritual Guide

[![Streamlit](https://img.shields.io/badge/Built%20With-Streamlit-blue?logo=streamlit)](https://streamlit.io/)
[![LLM](https://img.shields.io/badge/LLM-Together.ai%20%7C%20Mixtral%208x7B-brightgreen)](https://www.together.ai)
[![ChromaDB](https://img.shields.io/badge/Vector%20DB-ChromaDB-purple)](https://www.trychroma.com/)
[![License](https://img.shields.io/github/license/vijaysheru/mythology)](https://github.com/vijaysheru/mythology)

> “You came into this world empty-handed, and you will leave empty-handed. What is yours today belonged to someone else yesterday.”  
> — *Bhagavad Gita*

---

## 🌟 Overview

**MythOS: Talk to Lord Krishna** is an AI-powered chatbot that lets users ask spiritual, personal, or philosophical questions and receive guidance inspired by the **Bhagavad Gita** — spoken in the voice of **Lord Krishna**.

✨ Features:
- 🔮 LLM-powered spiritual answers via Together.ai (Mixtral-8x7B)
- 📜 Automatic Gita verse quoting by topic (dharma, karma, etc.)
- 🗣️ Text-to-speech: Krishna *speaks* the answer to you
- 🧠 Chat memory: Krishna remembers your past questions
- 📁 Upload PDF or CSV with questions and get responses in bulk
- 🙏 Karma tracker (easter egg!)


## 🚀 Tech Stack

| Component       | Technology           |
|----------------|----------------------|
| 🧠 LLM          | Together.ai (Mixtral)|
| 🎨 Frontend     | Streamlit            |
| 📚 Gita Quotes  | Custom quotes module |
| 🗃️ Memory       | JSON + ChromaDB ready|
| 🔊 TTS          | gTTS (Google TTS)    |
| 📤 Uploads      | PDF/CSV with PyPDF2, pandas |

---

## 🛠️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/vijaysheru/mythology.git
cd mythology
```

### 2. Create virtual environment and install dependencies

```bash
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Set up `.env` file

Create a `.env` file in the root directory and add your Together.ai API key:

```env
OPENAI_API_KEY=your-together-api-key
```

### 4. Run the app

```bash
streamlit run frontend/app.py
```

---

## 🧪 Example Questions to Ask Krishna

- "What is dharma?"
- "Why do we suffer in life?"
- "How do I control my desires?"
- "Can you explain karma with a verse from the Gita?"
- "How to remain detached while fulfilling responsibilities?"

---

## 🧘 Credits & Philosophy

- 📖 **Bhagavad Gita** (transliteration + interpretation)
- 🕉️ Voice and tone inspired by Lord Krishna’s teachings to Arjuna
- 🙏 Open-source AI contributions and Together.ai for open model access

---

## 🔮 Roadmap

- [x] LLM-powered Krishna chatbot
- [x] Gita verse integration
- [x] Voice responses
- [x] Memory via chat history
- [x] Upload support (PDF/CSV)
- [ ] ChromaDB-based spiritual memory
- [ ] CrewAI agent with tools
- [ ] Mobile app (Flutter)
- [ ] Hugging Face or Streamlit deployment

---

## 📄 License

MIT License © [Vijay Sheru](https://github.com/vijaysheru)
