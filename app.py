import streamlit as st
import requests
import json

# --- 1. CONFIG & API KEY ---
API_KEY = st.secrets["OPENROUTER_API_KEY"]

st.set_page_config(page_title="Business English Tutor", page_icon="🎓")
st.title("📞 Business English: Telephoning & Feedback")

# --- 2. SCENARIOS (WITH VOCAB FROM CORNELSEN/KLETT) ---
st.sidebar.header("Lesson Settings")
scenario_key = st.sidebar.selectbox(
    "Select Scenario:",
    ["Inquiry (Trade Fair)", "Late Delivery (Complaint)", "Booking a Meeting"]
)

scenarios = {
    "Inquiry (Trade Fair)": {
        "role": "You are Mr. Miller from 'Eco-Tech'. A student calls because they saw your booth at a trade fair. You expect them to ask for a comprehensive catalogue and a favourable quotation. Be polite but insist on professional language.",
        "start": "Eco-Tech Germany, Mr. Miller speaking. How can I help you?",
        "vocab": ["trade fair", "booth", "catalogue", "quotation", "delivery period"]
    },
    "Late Delivery (Complaint)": {
        "role": "You are Ms. Henderson. You are quite strict. A customer calls about a late delivery. You need their order number and won't help until they are professional.",
        "start": "Westfield Logistics, Ms. Henderson. Who is calling, please?",
        "vocab": ["complaint", "delay", "order number", "dispatch", "apologize"]
    },
     "Booking a Meeting": {
        "role": "You are an assistant. The student wants a meeting with the CEO. You are very busy. Negotiate a date.",
        "start": "CEO's Office, how can I help you?",
        "vocab": ["appointment", "available", "postpone", "confirm", "suit you"]
    }
}

# --- 3. INITIALIZATION ---
if "messages" not in st.session_state or st.sidebar.button("Restart Conversation"):
    selected = scenarios[scenario_key]
    st.session_state.messages = [
        {"role": "system", "content": f"{selected['role']} Keep answers short. If student uses slang, correct them politely."},
        {"role": "assistant", "content": selected['start']}
    ]

# --- 4. DISPLAY CHAT ---
for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# --- 5. USER INPUT & AI RESPONSE ---
if prompt := st.chat_input("Your message..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # API Request
    payload = {
        "model": "meta-llama/llama-3-8b-instruct",
        "messages": st.session_state.messages,
        "max_tokens": 150
    }
    response = requests.post("https://openrouter.ai/api/v1/chat/completions", 
                             headers={"Authorization": f"Bearer {API_KEY}"}, 
                             json=payload)
    
    if response.status_code == 200:
        reply = response.json()['choices'][0]['message']['content']
        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.rerun()

# --- 6. FEEDBACK SECTION (THE 'TEACHER' PART) ---
st.divider()
if st.button("📊 Get Feedback / Gespräch auswerten"):
    with st.spinner("Dein persönlicher Lehrer analysiert das Gespräch..."):
        # Wir schicken den gesamten Chatverlauf an die KI für eine Analyse
        transcript = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages])
        
        analysis_prompt = f"""
        Analyze this English business phone call transcript. 
        1. List which of these keywords were used: {scenarios[scenario_key]['vocab']}.
        2. Evaluate politeness (Good: 'May I', 'Could you'; Bad: 'I want', 'Hey').
        3. Give 3 tips for improvement in German.
        
        Transcript:
        {transcript}
        """
        
        analysis_payload = {
            "model": "meta-llama/llama-3-8b-instruct",
            "messages": [{"role": "user", "content": analysis_prompt}]
        }
        
        ana_res = requests.post("https://openrouter.ai/api/v1/chat/completions", 
                                headers={"Authorization": f"Bearer {API_KEY}"}, 
                                json=analysis_payload)
        
        if ana_res.status_code == 200:
            feedback = ana_res.json()['choices'][0]['message']['content']
            st.success("### Dein Feedback")
            st.markdown(feedback)
