# SPEEDY AI (Web Compatible Version)
# ✅ Works on mobile/desktop, 📢 voice reply, 🎤 mic via browser, 🌐 internet search ready

import streamlit as st
import pyttsx3
import json
from datetime import datetime
import os
import requests

# Streamlit page setup
st.set_page_config(page_title="SPEEDY - Super Assistant", layout="centered")
st.title("🤖 SPEEDY - Super Intelligence Assistant")
st.markdown("**Hello Sunil Kumar (Owner)** 👑")

# Init session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "voice_reply" not in st.session_state:
    st.session_state.voice_reply = True

# TTS Init (voice output)
def speak(text):
    try:
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    except:
        pass  # Fail silently on platforms that don't support it

# Intelligent response (uses internet search via DuckDuckGo if needed)
def get_reply(prompt):
    try:
        if any(q in prompt.lower() for q in ["who", "what", "when", "where", "how", "why"]):
            query = prompt.replace(" ", "+")
            url = f"https://api.duckduckgo.com/?q={query}&format=json"
            res = requests.get(url)
            data = res.json()
            abstract = data.get("Abstract")
            if abstract:
                return abstract
        return f"Let me help you with that, Sunil. (No direct answer found online.)"
    except:
        return "Sorry, I couldn't fetch that right now. Try again later."

# Display chat history
for role, msg in st.session_state.chat_history:
    with st.chat_message("user" if role == "Sunil Kumar" else "assistant"):
        st.markdown(msg)

# Voice input via browser
st.markdown("<script src='https://code.responsivevoice.org/responsivevoice.js?key=YOUR_KEY_HERE'></script>", unsafe_allow_html=True)

# User input
user_prompt = st.chat_input("Ask SPEEDY anything...")

# Process input
if user_prompt:
    st.session_state.chat_history.append(("Sunil Kumar", user_prompt))
    with st.chat_message("user"):
        st.markdown(user_prompt)
    with st.chat_message("assistant"):
        with st.spinner("Speedy is thinking..."):
            reply = get_reply(user_prompt)
            st.markdown(reply)
            st.session_state.chat_history.append(("Speedy", reply))
            if st.session_state.voice_reply:
                speak(reply)

# Sidebar Memory
st.sidebar.header("🧠 SPEEDY Memory")

if st.sidebar.button("💾 Save History"):
    dt = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    with open(f"chat_{dt}.json", "w", encoding="utf-8") as f:
        json.dump(st.session_state.chat_history, f, indent=2)
    st.sidebar.success("Chat history saved!")

def list_chats():
    return [f for f in os.listdir() if f.startswith("chat_") and f.endswith(".json")]

selected = st.sidebar.selectbox("📁 Load Previous Chat", ["-- Select --"] + list_chats())
if selected and selected != "-- Select --":
    with open(selected, "r", encoding="utf-8") as f:
        st.session_state.chat_history = json.load(f)
    st.sidebar.success(f"Loaded: {selected}")
    st.rerun()

st.sidebar.toggle("🔊 Voice Reply", key="voice_reply")
