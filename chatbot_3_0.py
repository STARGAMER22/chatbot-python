import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.title("🤖 Chatbot 3.0")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    st.chat_message(message["role"]).write(message["content"])

user_input = st.chat_input("Écris un message...")

if user_input:
    st.session_messages.append({"role": "user", "content": user_input})

    st.chat_message("user").write(user_input)

    response = client.response.create(
        model="gpt-4.1-mini",
        input=user_input
    )

    reply = response.output_text

    st.session_state.message.append({"role": "assistant", "content": reply})

    st.chat_message("assistant").write(reply)
