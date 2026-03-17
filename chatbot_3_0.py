import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(page_title="Chatbot 5.0", page_icon="🤖")

# 🌙 thème
theme = st.sidebar.toggle("🌙 Mode sombre")

if theme:
    st.markdown(
        "<style>body {background-color: #0e1117; color: white;}</style>",
        unsafe_allow_html=True
    )

# 👤 pseudo utilisateur
username = st.sidebar.text_input("Ton pseudo", "Invité")

# 📁 sauvegarde
SAVE_FILE = "conversations.json"

def save_data(data):
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f)

def load_data():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            return json.load(f)
    return {}

data = load_data()

if username not in data:
    data[username] = []

# 🎛️ mode
mode = st.sidebar.radio("Mode :", ["Texte 💬", "Image 🎨"])

st.title(f"🤖 Chatbot 5.0 - {username}")

# historique
messages = data[username]

# affichage
for msg in messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if "image" in msg:
            st.image(msg["image"])

# entrée
user_input = st.chat_input("Écris ici...")

if user_input:

    messages.append({"role": "user", "content": user_input})

    st.chat_message("user").write(user_input)

    # TEXTE
    if mode == "Texte 💬":

        response = client.responses.create(
            model="gpt-4.1-mini",
            input=user_input
        )

        reply = response.output_text

        messages.append({
            "role": "assistant",
            "content": reply
        })

        st.chat_message("assistant").write(reply)

    # IMAGE
    else:

        with st.chat_message("assistant"):
            st.write("🎨 Génération en cours...")

        result = client.images.generate(
            model="gpt-image-1",
            prompt=user_input,
            size="1024x1024"
        )

        image_url = result.data[0].url

        messages.append({
            "role": "assistant",
            "content": "Image générée",
            "image": image_url
        })

        with st.chat_message("assistant"):
            st.image(image_url)

    save_data(data)
