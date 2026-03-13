import tkinker as tk
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def envoyer():
    message = entree.get()
    entree.delete(0, tk.END)

    # bulle utilisateur (jaune)
    chat.insert(tk.END, "Toi : " + message +"/n", "user")

    response = client.responses.craete(
        model="gpt-4.1-mini"
        input=message
    )

    
        
