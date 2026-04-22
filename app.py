import streamlit as st
import requests
import json

# --- 1. CONFIG ---
API_KEY = st.secrets["OPENROUTER_API_KEY"]

st.set_page_config(page_title="Business English Tutor", page_icon="🎓")
st.title("📞 Business English: Telephoning & Feedback")

# --- 2. SCENARIOS ---
st.sidebar.header("Unterrichts-Einstellungen")
scenario_key = st.sidebar.selectbox(
    "Szenario wählen:",
    ["Inquiry (Trade Fair)", "Late Delivery (Complaint)", "Booking a Meeting"]
)

scenarios = {
    "Inquiry (Trade Fair)": {
        "role": "You are Mr. Miller from 'Eco-Tech'. A student calls because they saw your booth at a trade fair. You expect them to ask for a catalogue. Be professional.",
        "start": "Eco-Tech Germany, Mr. Miller speaking. How can I help you?",
        "vocab": ["trade fair", "booth", "catalogue", "quotation", "delivery period"]
    },
    "Late Delivery (Complaint)": {
        "role": "You are Ms. Henderson, a strict receptionist. A student calls about a late delivery. You need an order number.",
        "start": "Westfield Logistics, Ms. Henderson. Who is calling, please?",
        "vocab": ["complaint", "delay", "order number", "dispatch", "apologize"]
    },
    "Booking a Meeting": {
        "role": "You are an assistant. The student wants a meeting with the CEO. Negotiate a date.",
        "start": "CEO's Office, how can I help you?",
        "vocab": ["appointment", "available", "postpone", "confirm", "suit you"]
    }
}

# --- 3. INITIALIZATION ---
if "messages" not in st.session_state or st.sidebar.button("Gespräch neu starten"):
    selected = scenarios[scenario_key]
    st.session_state.messages = [
        {"role": "system", "content": f"{selected['role']} Keep answers very short. If the student is too informal, tell them."},
        {"role": "assistant", "content": selected['start']}
    ]

# --- 4. DISPLAY CHAT ---
for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# --- 5. USER INPUT ---
if prompt := st.chat_input("Schreibe hier deine Antwort..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    payload = {
        "model": "meta-llama/llama-3-8b-instruct",
        "messages": st.session_state.messages,
        "max_tokens": 100
    }
    response = requests.post("https://openrouter.ai/api/v1/chat/completions", 
                             headers={"Authorization": f"Bearer {API_KEY}"}, json=payload)
    
    if response.status_code == 200:
        reply = response.json()['choices'][0]['message']['content']
        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.rerun()

# --- 6. VERBESSERTES FEEDBACK-MODUL ---
st.divider()
if st.button("📊 Gespräch auswerten (Lehrer-Feedback)"):
    with st.spinner("Dein Tutor analysiert deine Leistung..."):
        
        # Wir filtern nur die Nachrichten des Schülers heraus
        student_performance = [m['content'] for m in st.session_state.messages if m['role'] == 'user']
        
        analysis_prompt = f"""
        Du bist ein erfahrener Englischlehrer an einem kaufmännischen Berufskolleg. 
        Analysiere die Leistung des Schülers in diesem Telefonat.
        
        WICHTIG: 
        - Schreibe dein Feedback komplett auf DEUTSCH.
        - Bewerte NUR die Nachrichten des Schülers (User). Ignoriere deine eigenen Antworten (Assistant).
        - Prüfe, ob diese Wörter verwendet wurden: {scenarios[scenario_key]['vocab']}.
        
        STRUKTUR des Feedbacks:
        1. Höflichkeit & Etikette (Hat er sich vorgestellt? War er formell genug?)
        2. Fachvokabular (Welche wichtigen Wörter wurden genutzt?)
        3. Verbesserungsvorschläge (Gib 3 konkrete Beispiele auf Englisch, wie er Sätze schöner formulieren könnte).
        
        Chat-Verlauf des Schülers:
        {student_performance}
        """
        
        analysis_payload = {
            "model": "meta-llama/llama-3-8b-instruct",
            "messages": [{"role": "user", "content": analysis_prompt}]
        }
        
        ana_res = requests.post("https://openrouter.ai/api/v1/chat/completions", 
                                headers={"Authorization": f"Bearer {API_KEY}"}, json=analysis_payload)
        
        if ana_res.status_code == 200:
            feedback = ana_res.json()['choices'][0]['message']['content']
            st.success("### Dein persönliches Feedback")
            st.markdown(feedback)
