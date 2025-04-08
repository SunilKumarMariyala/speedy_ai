# SPEEDY AI: Voice Chat + Intelligent Responses + Auto History

import streamlit as st
import subprocess
import os
import tempfile
import pyttsx3
import whisper
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
from PyPDF2 import PdfReader
from datetime import datetime
import json

st.set_page_config(page_title="Speedy AI", layout="wide")
st.title("🤖 SPEEDY - Super Intelligence Assistant")
st.markdown("**Hello Sunil Kumar (Owner)** 👑")

# Load Whisper model
model = whisper.load_model("base")

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Text-to-speech
engine = pyttsx3.init()
engine.setProperty('voice', 'HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_EN-US_DAVID_11.0')
def speak(text):
    try:
        engine.say(text)
        engine.runAndWait()
    except RuntimeError:
        pass

# Use Llama3 via Ollama
def ask_speedy(prompt):
    result = subprocess.run(
        ["ollama", "run", "llama3"],
        input=prompt.encode(),
        stdout=subprocess.PIPE
    )
    return result.stdout.decode().strip()

# PDF Reader
def read_pdf(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# Record and transcribe voice
def record_voice(duration=5, fs=44100):
    st.info("🎙️ Listening... Speak now.")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()
    temp_wav = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    write(temp_wav.name, fs, audio)
    return temp_wav.name

def transcribe_audio(path):
    result = model.transcribe(path)
    return result["text"]

# Input via typing or mic
col1, col2 = st.columns([3, 1])
with col1:
    prompt = st.chat_input("Ask Speedy anything...")
with col2:
    if st.button("🎤 Talk to Speedy"):
        audio_path = record_voice()
        prompt = transcribe_audio(audio_path)

# Handle input and generate reply
if prompt:
    st.session_state.chat_history.append(("Sunil Kumar", prompt))
    with st.spinner("Speedy is thinking..."):
        reply = ask_speedy(prompt)
    st.session_state.chat_history.append(("Speedy", reply))
    speak(reply)
    st.rerun()  # to refresh display with updated chat

# Display chat history with Streamlit chat style
for role, text in st.session_state.chat_history:
    with st.chat_message("user" if role == "Sunil Kumar" else "assistant"):
        st.markdown(f"**{role}:** {text}")

# Sidebar
st.sidebar.title("📁 Upload Files & Save")

uploaded_file = st.sidebar.file_uploader("Choose a PDF or TXT file", type=["pdf", "txt"])
if uploaded_file:
    if uploaded_file.type == "application/pdf":
        text = read_pdf(uploaded_file)
    else:
        text = uploaded_file.read().decode("utf-8")
    st.session_state.chat_history.append(("[File Content]", text[:1000]))
    st.sidebar.success("File uploaded. Preview added to chat.")

# Auto-save chat history every run
def auto_save_chat():
    os.makedirs("chat_history", exist_ok=True)
    dt = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filepath = os.path.join("chat_history", f"chat_{dt}.json")
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(st.session_state.chat_history, f, indent=2)

auto_save_chat()

# Load and display saved chats
def list_chats():
    if not os.path.exists("chat_history"):
        return []
    return sorted([f for f in os.listdir("chat_history") if f.endswith(".json")], reverse=True)

selected_chat = st.sidebar.selectbox("📜 Load Previous Chat", ["-- Select --"] + list_chats())
if selected_chat != "-- Select --":
    with open(os.path.join("chat_history", selected_chat), "r", encoding="utf-8") as f:
        st.session_state.chat_history = json.load(f)
    st.sidebar.success(f"Loaded: {selected_chat}")
    st.rerun()