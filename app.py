import streamlit as st
from openai import OpenAI
import requests

# UI Instellingen
st.set_page_config(page_title="Paman & Neefje", page_icon="❤️")
st.title("🇳🇱 Vertaler 🇮🇩")

# API Keys (Deze kun je veilig invullen in de Streamlit 'Secrets' instellingen)
OPENAI_API_KEY = st.sidebar.text_input("OpenAI API Key", type="password")
ELEVENLABS_API_KEY = st.sidebar.text_input("ElevenLabs API Key", type="password")

client = OpenAI(api_key=OPENAI_API_KEY)

def speak(text, voice_id):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {"xi-api-key": ELEVENLABS_API_KEY, "Content-Type": "application/json"}
    data = {"text": text, "model_id": "eleven_multilingual_v2", "voice_settings": {"stability": 0.4, "similarity_boost": 0.75}}
    response = requests.post(url, json=data, headers=headers)
    return response.content

# --- MODUS 1: Oom spreekt ---
st.subheader("Oom spreekt (NL ➔ ID)")
audio_oom = st.audio_input("Spreek in voor je neefje", key="oom")

if audio_oom:
    # Transcriptie & Vertaling
    transcript = client.audio.transcriptions.create(model="whisper-1", file=audio_oom)
    vertaling = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": "Vertaal naar simpel Indonesisch voor een kind van 2. Gebruik woorden als 'Halo', 'Sayang', 'Main'."},
                  {"role": "user", "content": transcript.text}]
    ).choices[0].message.content
    
    st.info(f"Je zei: {transcript.text}")
    st.success(f"Vertaling: {vertaling}")
    
    # ElevenLabs "George" ID (voorbeeld)
    audio_data = speak(vertaling, "JBFivEUD9SvSCNo9n93u") 
    st.audio(audio_data, format="audio/mp3", autoplay=True)

st.divider()

# --- MODUS 2: Neefje spreekt ---
st.subheader("Neefje spreekt (ID ➔ NL)")
audio_neef = st.audio_input("Laat je neefje praten", key="neefje")

if audio_neef:
    transcript = client.audio.transcriptions.create(model="whisper-1", file=audio_neef)
    vertaling = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": "Vertaal dit Indonesisch van een peuter naar natuurlijk Nederlands."},
                  {"role": "user", "content": transcript.text}]
    ).choices[0].message.content
    
    st.info(f"Neefje zei: {transcript.text}")
    st.success(f"Betekenis: {vertaling}")
    
    # ElevenLabs "Gigi" ID (voorbeeld)
    audio_data = speak(vertaling, "jBpf6oByH17zmcU9ag9") 
    st.audio(audio_data, format="audio/mp3", autoplay=True)
