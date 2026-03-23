import streamlit as st
from google import genai
from google.genai import types

# ── Config ──────────────────────────────────────────────
API_KEY = "AIzaSyBRxz-67YodnOxAZJ5JKXooQUH5SqaGkno"
KB_FILE = "Chernobyl.txt"
MODEL   = "gemini-2.5-flash"

# ── Load KB once ────────────────────────────────────────
if "kb" not in st.session_state:
    with open(KB_FILE, "r") as f:
        st.session_state.kb = f.read()

SYSTEM_PROMPT = f"""
You are an journalist who knows about the major incidents happpened all over the world.Your job is to provide required information asked by the user and
you should answer them in polite manner,if there is any questions out of your knowledge say you dont have info about it.
{st.session_state.kb}
"""

# ── Session state for display + API history ──────────────
if "messages" not in st.session_state:
    st.session_state.messages = []        # for display
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []    # for API (types.Content list)

def send_message(user_text):
    # Fresh client every time — avoids httpx closed-client error
    client = genai.Client(api_key=API_KEY)
    chat = client.chats.create(
        model=MODEL,
        config={"system_instruction": SYSTEM_PROMPT},
        history=st.session_state.chat_history   # replay full history
    )
    response = chat.send_message(user_text)

    # Save updated history for next turn
    st.session_state.chat_history = chat.get_history()
    return response.text

# ── App ──────────────────────────────────────────────────
st.title("Chernobyl Journalist Chatbot")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if user_input := st.chat_input("Ask me about Chernobyl..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    reply = send_message(user_input)

    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.write(reply)
