import streamlit as st
import os
import json
import pandas as pd
from PyPDF2 import PdfReader
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
import tempfile
import sys

# Allow backend import
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from backend.krishna_agent import get_krishna_response

# Load environment variables
load_dotenv()
api_key = os.getenv("ELEVEN_API_KEY")  # 🔐 For ElevenLabs TTS

# File paths
KARMA_FILE = "memory/karma.json"
CHAT_HISTORY_FILE = "memory/chat_history.json"

# Set page config
st.set_page_config(page_title="MythOS: Talk to Krishna", page_icon="🕉️")
st.title("🕉️ Talk to Lord Krishna")
st.markdown("Ask me anything — from spiritual doubts to life's biggest decisions.")

# --- Init files ---
def initialize_files():
    os.makedirs("memory", exist_ok=True)
    if not os.path.exists(KARMA_FILE):
        with open(KARMA_FILE, "w") as f:
            json.dump({"karma": 0}, f)
    if not os.path.exists(CHAT_HISTORY_FILE):
        with open(CHAT_HISTORY_FILE, "w") as f:
            json.dump([], f)

initialize_files()

# --- Karma update ---
def update_karma():
    with open(KARMA_FILE, "r") as f:
        data = json.load(f)
    data["karma"] += 1
    with open(KARMA_FILE, "w") as f:
        json.dump(data, f)

# --- Memory logging ---
def log_chat(question, answer):
    with open(CHAT_HISTORY_FILE, "r") as f:
        history = json.load(f)
    history.append({"question": question, "answer": answer})
    with open(CHAT_HISTORY_FILE, "w") as f:
        json.dump(history[-20:], f, indent=2)

def load_past_questions():
    try:
        with open(CHAT_HISTORY_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []

# --- Text-to-Speech (ElevenLabs) ---
def play_krishna_voice(text):
    if not api_key:
        st.warning("⚠️ ELEVEN_API_KEY not set in environment or secrets.")
        return

    try:
        client = ElevenLabs(api_key=api_key)
        audio_stream = client.generate(
            text=text,
            voice="Arnold",  # Try "Antoni", "Adam", or custom
            model="eleven_monolingual_v1",
            stream=True
        )
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            for chunk in audio_stream:
                tmp.write(chunk)
            st.audio(tmp.name, format="audio/mp3")
    except Exception as e:
        st.error(f"🛑 Voice generation failed: {e}")

# --- Upload handling ---
def extract_questions(file):
    if file.name.endswith(".pdf"):
        reader = PdfReader(file)
        return [page.extract_text().strip() for page in reader.pages if page.extract_text()]
    elif file.name.endswith(".csv"):
        df = pd.read_csv(file)
        return df.iloc[:, 0].dropna().tolist()
    return []

# --- Sidebar Memory ---
st.sidebar.title("📜 Past Questions")
for chat in load_past_questions():
    st.sidebar.markdown(f"**Q:** {chat['question']}  \n**A:** {chat['answer'][:100]}...")

# --- Upload UI ---
uploaded_file = st.file_uploader("📁 Upload a PDF or CSV with questions", type=["pdf", "csv"])

if uploaded_file:
    st.success("File uploaded. Krishna will answer your questions:")
    questions = extract_questions(uploaded_file)
    for q in questions:
        update_karma()
        with st.spinner("Krishna is reflecting..."):
            response = get_krishna_response(q)
        st.markdown(f"**🙏 You asked:** {q}")
        st.markdown(f"**🕉️ Krishna:** {response}")
        play_krishna_voice(response)
        log_chat(q, response)

# --- Single user question ---
user_input = st.text_input("🙏 Your Question to Krishna:")

if user_input:
    update_karma()
    with st.spinner("Krishna is thinking..."):
        response = get_krishna_response(user_input)
    st.markdown(f"**🕉️ Krishna:** {response}")
    play_krishna_voice(response)
    log_chat(user_input, response)
