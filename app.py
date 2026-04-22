import streamlit as st
import requests
import json

# 1. Konfiguration & Sicherheit
API_KEY = st.secrets["OPENROUTER_API_KEY"]

st.set_page_config(page_title="Business English Trainer", page_icon="📞")
st.title("📞 Business English Telephoning Simulation")

# 2. Auswahl des Szenarios durch den Schüler
st.sidebar.header("Übungseinstellungen")
scenario = st.sidebar.selectbox(
    "Wähle dein Szenario aus:",
    [
        "Late Delivery (Complaint)",
        "Booking a Meeting",
        "General Inquiry"
    ]
)

# 3. Definition der Prompts basierend auf dem Szenario
prompts = {
    "Late Delivery (Complaint)": {
        "role_desc": "You are Ms. Henderson, a strict receptionist. A customer calls because a delivery is late. You need an order number and remain professional but firm.",
        "start_msg": "Westfield Logistics, Ms. Henderson speaking. How can I help you?"
    },
    "Booking a Meeting": {
        "role_desc": "You are the assistant to Mr. Miller. The student wants to book a meeting. You are very busy and need to negotiate a date.",
        "start_msg": "Office of Mr. Miller, speaking. What can I do for you today?"
    },
    "General Inquiry": {
        "role_desc": "You are a sales agent. The student asks for a catalogue. You must ask for their company name and business address first.",
        "start_msg": "Global Solutions Sales Team. How may I assist you?"
    }
}

# 4. Chat-Historie initialisieren (wird zurückgesetzt, wenn das Szenario gewechselt wird)
if "messages" not in st.session_state or st.sidebar.button("Gespräch neu starten"):
    selected = prompts[scenario]
    st.session_state.messages = [
        {"role": "system", "content": f"{selected['role_desc']} ONLY accept formal English. If the student is informal, ask them to stay professional. Keep answers short."},
        {"role": "assistant", "content": selected['start_msg']}
    ]

# 5. Chat-Anzeige
for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 6. User Input & KI-Antwort
if prompt := st.chat_input("Type your message..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    headers = {"Authorization": f"Bearer {API_KEY}"}
    payload = {
        "model": "meta-llama/llama-3-8b-instruct",
        "messages": st.session_state.messages,
        "max_tokens": 150
    }
    
    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
    
    if response.status_code == 200:
        reply = response.json()['choices'][0]['message']['content']
        st.session_state.messages.append({"role": "assistant", "content": reply})
        with st.chat_message("assistant"):
            st.write(reply)
    else:
        st.error("Connection error. Check your API key or internet.")
