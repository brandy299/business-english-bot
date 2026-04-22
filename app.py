import streamlit as st
import requests
from scenarios import SCENARIOS

# --- CONFIGURATION & DESIGN ---
st.set_page_config(
    page_title="Business English Bot - CYBERPUNK", 
    page_icon="🤖", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for "Lovable" Cyberpunk Aesthetic
st.markdown("""
<style>
    /* Main Background with a subtle gradient */
    .stApp {
        background: radial-gradient(circle at top, #1a1a2e 0%, #0a0a0c 100%);
        color: #e0e0e0;
    }
    
    /* Extreme Neon Header */
    h1 {
        color: #00f2ff !important;
        text-shadow: 0 0 20px #00f2ff, 0 0 40px #7000ff;
        font-family: 'Segoe UI', sans-serif;
        text-transform: uppercase;
        letter-spacing: 2px;
        text-align: center;
        padding: 20px;
        border: 2px solid #00f2ff;
        border-radius: 15px;
        box-shadow: inset 0 0 15px rgba(0, 242, 255, 0.2), 0 0 15px rgba(0, 242, 255, 0.2);
    }

    /* Georgia Font for Academic Content */
    .academic-text {
        font-family: 'Georgia', serif;
        font-size: 1.2rem;
        line-height: 1.6;
        color: #ffffff;
        background: rgba(0, 242, 255, 0.05);
        padding: 25px;
        border-radius: 10px;
        border-left: 5px solid #7000ff;
        box-shadow: 5px 5px 15px rgba(0,0,0,0.5);
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #050505 !important;
        border-right: 2px solid #7000ff;
    }

    /* Chat Bubbles Modernized */
    [data-testid="stChatMessage"] {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(112, 0, 255, 0.3) !important;
        border-radius: 20px !important;
        padding: 15px !important;
        margin-bottom: 15px !important;
        transition: 0.3s;
    }
    [data-testid="stChatMessage"]:hover {
        border-color: #00f2ff !important;
        box-shadow: 0 0 10px rgba(0, 242, 255, 0.2);
    }

    /* Buttons with Glow */
    .stButton>button {
        background: linear-gradient(45deg, #00f2ff, #7000ff) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: bold !important;
        padding: 10px 25px !important;
        text-transform: uppercase;
    }
    .stButton>button:hover {
        box-shadow: 0 0 25px #00f2ff !important;
        transform: translateY(-2px);
    }
</style>
""", unsafe_allow_html=True)

# --- API HELPERS ---
def get_completion(messages, model="meta-llama/llama-3-8b-instruct"):
    try:
        API_KEY = st.secrets["OPENROUTER_API_KEY"]
        res = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={"Authorization": f"Bearer {API_KEY}"},
            json={"model": model, "messages": messages, "max_tokens": 150}
        )
        return res.json()['choices'][0]['message']['content']
    except Exception as e:
        return f"Error: {str(e)}"

# --- SIDEBAR ---
with st.sidebar:
    st.title("⚡ English Coach")
    st.markdown("---")
    selected_scenario_name = st.selectbox("CHOOSE YOUR MISSION:", list(SCENARIOS.keys()))
    current = SCENARIOS[selected_scenario_name]
    
    st.markdown("### ⚡ SYSTEM TOOLS")
    if st.button("RESET SIMULATION"):
        st.session_state.messages = [
            {"role": "system", "content": f"{current['system_prompt']} Keep answers short and professional."},
            {"role": "assistant", "content": current['start_msg']}
        ]
        st.rerun()

# --- MAIN UI ---
st.title("🚀 Business English Telephoning Trainer")

col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("### 📋 MISSION BRIEFING")
    st.markdown(f'<div class="academic-text">{current["task"]}</div>', unsafe_allow_html=True)
    
    st.markdown("### 💾 KEY VOCABULARY")
    for word in current['vocab']:
        st.markdown(f"🔹 **{word}**")

with col2:
    # --- CHAT INITIALIZATION ---
    if "messages" not in st.session_state or st.session_state.get('last_scenario') != selected_scenario_name:
        st.session_state.messages = [
            {"role": "system", "content": f"{current['system_prompt']} Keep answers short and professional."},
            {"role": "assistant", "content": current['start_msg']}
        ]
        st.session_state.last_scenario = selected_scenario_name

    # --- CHAT DISPLAY ---
    chat_container = st.container(height=500)
    with chat_container:
        for msg in st.session_state.messages[1:]:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

    # --- USER INPUT ---
    if prompt := st.chat_input("Input command..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with chat_container:
            with st.chat_message("user"):
                st.write(prompt)
            
            with st.chat_message("assistant"):
                with st.spinner("PROCESSING DATA..."):
                    response = get_completion(st.session_state.messages)
                    st.write(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})

# --- FEEDBACK SECTION ---
st.markdown("---")
if st.button("📊 GENERATE PERFORMANCE REPORT"):
    student_msgs = [m['content'] for m in st.session_state.messages if m['role'] == 'user']
    if not student_msgs:
        st.warning("Please start the conversation first!")
    else:
        with st.spinner("ANALYZING PROTOCOLS..."):
            analysis_prompt = f"""
            Analysiere als Englischlehrer diesen Chat-Verlauf eines Schülers (User).
            Schreibe auf DEUTSCH. Nutze Markdown für die Struktur.
            1. **Höflichkeit**: Wurden formelle Phrasen genutzt?
            2. **Vokabeln**: Wurden diese Wörter korrekt genutzt: {current['vocab']}?
            3. **Verbesserung**: 3 konkrete englische Sätze, wie der Schüler es besser hätte sagen können.
            Verlauf: {student_msgs}
            """
            feedback = get_completion([{"role": "user", "content": analysis_prompt}])
            st.success("### 📝 Performance Report")
            st.markdown(feedback)
