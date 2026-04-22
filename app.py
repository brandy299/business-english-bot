import streamlit as st
import requests
from scenarios import SCENARIOS

# --- CONFIGURATION & DESIGN ---
st.set_page_config(
    page_title="Business English Bot", 
    page_icon="📞", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for "Lovable" Cyberpunk Aesthetic
st.markdown("""
<style>
    /* Main Background */
    .stApp {
        background-color: #0a0a0c;
        color: #e0e0e0;
    }
    
    /* Neon Glow for Headers */
    h1, h2, h3 {
        color: #00f2ff !important;
        text-shadow: 0 0 10px rgba(0, 242, 255, 0.5);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    /* Georgia Font for Academic Content */
    .academic-text {
        font-family: 'Georgia', serif;
        font-size: 1.1rem;
        line-height: 1.6;
        color: #d1d1d1;
        background: rgba(255, 255, 255, 0.05);
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #00f2ff;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #111114 !important;
        border-right: 1px solid #333;
    }

    /* Chat Bubbles */
    [data-testid="stChatMessage"] {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(0, 242, 255, 0.1);
        border-radius: 15px;
        margin-bottom: 10px;
    }

    /* Buttons */
    .stButton>button {
        background: linear-gradient(90deg, #00f2ff, #7000ff);
        color: white;
        border: none;
        border-radius: 5px;
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton>button:hover {
        box-shadow: 0 0 15px rgba(0, 242, 255, 0.6);
        transform: scale(1.02);
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
    st.title("🤖 English Coach")
    st.markdown("---")
    selected_scenario_name = st.selectbox("Select Scenario:", list(SCENARIOS.keys()))
    current = SCENARIOS[selected_scenario_name]
    
    st.markdown("### 🛠 Tools")
    if st.button("🔄 Restart Conversation"):
        st.session_state.messages = [
            {"role": "system", "content": f"{current['system_prompt']} Keep answers short and professional."},
            {"role": "assistant", "content": current['start_msg']}
        ]
        st.rerun()

# --- MAIN UI ---
st.title("📞 Business English Telephoning Trainer")

col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("### 📖 Instructions")
    st.markdown(f'<div class="academic-text">{current["task"]}</div>', unsafe_allow_html=True)
    
    st.markdown("### 🔑 Vocabulary")
    for word in current['vocab']:
        st.markdown(f"- `{word}`")

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
    if prompt := st.chat_input("Type your response here..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with chat_container:
            with st.chat_message("user"):
                st.write(prompt)
            
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = get_completion(st.session_state.messages)
                    st.write(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})

# --- FEEDBACK SECTION ---
st.markdown("---")
if st.button("📊 Analyze My Performance"):
    student_msgs = [m['content'] for m in st.session_state.messages if m['role'] == 'user']
    if not student_msgs:
        st.warning("Please start the conversation first!")
    else:
        with st.spinner("Analyzing..."):
            analysis_prompt = f"""
            Analysiere als Englischlehrer diesen Chat-Verlauf eines Schülers (User).
            Schreibe auf DEUTSCH. Nutze Markdown für die Struktur.
            1. **Höflichkeit**: Wurden formelle Phrasen genutzt?
            2. **Vokabeln**: Wurden diese Wörter korrekt genutzt: {current['vocab']}?
            3. **Verbesserung**: 3 konkrete englische Sätze, wie der Schüler es besser hätte sagen können.
            Verlauf: {student_msgs}
            """
            feedback = get_completion([{"role": "user", "content": analysis_prompt}])
            st.success("### 📝 Teacher's Feedback")
            st.markdown(feedback)
