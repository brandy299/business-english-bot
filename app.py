import streamlit as st
import requests
import json

# Konfiguration über Streamlit Secrets (Datenschutz!)
API_KEY = st.secrets["OPENROUTER_API_KEY"]

st.set_page_config(page_title="Telephoning Trainer", page_icon="📞")
st.title("📞 Business English Telephoning Simulation")
st.markdown("### Scenario: Calling Ms. Henderson at Westfield Logistics")

# Initialisierung des Chats
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are Ms. Henderson, a professional and strict receptionist in Manchester. ONLY accept formal English. If the student is informal (Hi, Hey, I want), react with: 'I'm sorry, I didn't quite catch that. Who is calling, please?' and insist on professional etiquette. Keep answers short like a real phone call."},
        {"role": "assistant", "content": "Westfield Logistics, Ms. Henderson speaking. How can I help you?"}
    ]

# Chat-Anzeige
for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# User Input
if prompt := st.chat_input("Type your response here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # API Anfrage an OpenRouter
    headers = {"Authorization": f"Bearer {API_KEY}"}
    payload = {
        "model": "meta-llama/llama-3-8b-instruct", # Kostengünstiges SLM
        "messages": st.session_state.messages
    }
    
    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
    
    if response.status_code == 200:
        reply = response.json()['choices'][0]['message']['content']
        st.session_state.messages.append({"role": "assistant", "content": reply})
        with st.chat_message("assistant"):
            st.write(reply)
    else:
        st.error("Connection error. Please try again.")
