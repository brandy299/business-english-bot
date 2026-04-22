import streamlit as st
import requests
import json

# --- 1. KONFIGURATION ---
API_KEY = st.secrets["OPENROUTER_API_KEY"]

st.set_page_config(page_title="Business English Bot", page_icon="🎓", layout="centered")
st.title("📞 Business English Telephoning Trainer")

# --- 2. SZENARIEN & ANWEISUNGEN ---
scenarios = {
    "Inquiry (Trade Fair)": {
        "task": """
        **Deine Aufgabe:** Du arbeitest bei der 'Westphalia Office GmbH'. Letzte Woche warst du auf einer Messe in Köln.
        1. Rufe bei 'Eco-Tech Germany' an und verlange Herrn Miller.
        2. Beziehe dich auf das Gespräch an ihrem Messestand (*booth*).
        3. Bitte um einen Katalog und ein Angebot (*quotation*).
        4. Frage nach den Lieferzeiten (*delivery period*).
        """,
        "system": "You are Mr. Miller from Eco-Tech. A student calls about a trade fair. Be professional.",
        "start_msg": "Eco-Tech Germany, Mr. Miller speaking. How can I help you?",
        "vocab": ["trade fair", "booth", "catalogue", "quotation", "delivery period"]
    },
    "Late Delivery (Complaint)": {
        "task": """
        **Deine Aufgabe:** Eine wichtige Lieferung von Bürostühlen ist überfällig. Dein Chef macht Druck.
        1. Rufe bei 'Westfield Logistics' an und verlange Ms. Henderson.
        2. Beschwere dich höflich aber bestimmt über die Verzögerung (*delay*).
        3. Halte eine fiktive Bestellnummer bereit (z.B. Order No. 455).
        4. Verlange eine schnelle Lösung.
        """,
        "system": "You are Ms. Henderson, a very strict and formal receptionist. Do not accept slang.",
        "start_msg": "Westfield Logistics, Ms. Henderson. Who is calling, please?",
        "vocab": ["complaint", "delay", "order number", "dispatch", "apologize"]
    }
}

# --- 3. SIDEBAR ---
st.sidebar.header("Menü")
selected_name = st.sidebar.selectbox("Szenario wählen:", list(scenarios.keys()))
current = scenarios[selected_name]

if st.sidebar.button("Gespräch neu starten"):
    st.session_state.messages = [
        {"role": "system", "content": f"{current['system']} Keep answers short."},
        {"role": "assistant", "content": current['start_msg']}
    ]
    st.rerun()

# --- 4. ARBEITSANWEISUNG (EXPANDER) ---
with st.expander("📖 DEINE ARBEITSANWEISUNG (Hier klicken)", expanded=True):
    st.markdown(current['task'])
    st.info(f"**Wichtige Vokabeln:** {', '.join(current['vocab'])}")

# --- 5. CHAT INITIALISIERUNG ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": f"{current['system']} Keep answers short."},
        {"role": "assistant", "content": current['start_msg']}
    ]

# --- 6. CHAT ANZEIGE ---
for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# --- 7. USER INPUT ---
if prompt := st.chat_input("Deine Antwort..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    payload = {
        "model": "meta-llama/llama-3-8b-instruct",
        "messages": st.session_state.messages,
        "max_tokens": 100
    }
    res = requests.post("https://openrouter.ai/api/v1/chat/completions", 
                        headers={"Authorization": f"Bearer {API_KEY}"}, json=payload)
    
    if res.status_code == 200:
        st.session_state.messages.append({"role": "assistant", "content": res.json()['choices'][0]['message']['content']})
        st.rerun()

# --- 8. FEEDBACK ---
st.divider()
if st.button("📊 Gespräch auswerten"):
    student_msgs = [m['content'] for m in st.session_state.messages if m['role'] == 'user']
    analysis_prompt = f"""
    Analysiere als Englischlehrer diesen Chat-Verlauf eines Schülers (User).
    Schreibe auf DEUTSCH.
    1. Höflichkeit: Wurden formelle Phrasen genutzt?
    2. Vokabeln: Wurden diese Wörter genutzt: {current['vocab']}?
    3. Tipps: 3 konkrete englische Verbesserungsvorschläge.
    Verlauf: {student_msgs}
    """
    ana_res = requests.post("https://openrouter.ai/api/v1/chat/completions", 
                            headers={"Authorization": f"Bearer {API_KEY}"}, 
                            json={"model": "meta-llama/llama-3-8b-instruct", "messages": [{"role": "user", "content": analysis_prompt}]})
    if ana_res.status_code == 200:
        st.success("### Dein Feedback")
        st.write(ana_res.json()['choices'][0]['message']['content'])
