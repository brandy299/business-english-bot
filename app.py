import streamlit as st
import requests
from scenarios import SCENARIOS

# --- CONFIGURATION ---
st.set_page_config(
    page_title="Business English Trainer", 
    page_icon="🎓", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- PROFESSIONAL ACADEMIC DESIGN (IMPECCABLE) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');

    /* Global Styles */
    .stApp {
        background-color: #f8fafc;
        color: #1e293b;
        font-family: 'Inter', sans-serif;
    }

    /* Main Header */
    h1 {
        font-family: 'Georgia', serif;
        color: #0f172a;
        font-weight: 700;
        font-size: 2.5rem !important;
        border-bottom: 2px solid #e2e8f0;
        padding-bottom: 1rem;
        margin-bottom: 2rem !important;
    }

    h2, h3 {
        color: #334155;
        font-weight: 600;
    }

    /* Academic Instruction Card */
    .instruction-card {
        background-color: #ffffff;
        padding: 2rem;
        border-radius: 8px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        margin-bottom: 2rem;
    }

    .instruction-header {
        font-family: 'Georgia', serif;
        font-size: 1.4rem;
        color: #1e40af;
        margin-bottom: 1rem;
        border-bottom: 1px solid #f1f5f9;
        padding-bottom: 0.5rem;
    }

    .instruction-body {
        font-family: 'Georgia', serif;
        font-size: 1.15rem;
        line-height: 1.7;
        color: #334155;
    }

    /* Vocabulary Tags */
    .vocab-tag {
        display: inline-block;
        background-color: #eff6ff;
        color: #1e40af;
        padding: 0.2rem 0.6rem;
        border-radius: 4px;
        font-size: 0.9rem;
        font-weight: 600;
        margin-right: 0.5rem;
        margin-bottom: 0.5rem;
        border: 1px solid #dbeafe;
    }

    /* Sidebar Refinement */
    section[data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1px solid #e2e8f0;
    }

    /* Chat Styling */
    [data-testid="stChatMessage"] {
        background-color: #ffffff !important;
        border: 1px solid #f1f5f9 !important;
        border-radius: 12px !important;
        padding: 1rem !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05) !important;
    }

    /* Buttons */
    .stButton>button {
        background-color: #1e40af !important;
        color: white !important;
        border-radius: 6px !important;
        border: none !important;
        padding: 0.5rem 1.5rem !important;
        font-weight: 600 !important;
        transition: all 0.2s ease;
    }
    .stButton>button:hover {
        background-color: #1e3a8a !important;
        box-shadow: 0 4px 12px rgba(30, 64, 175, 0.2) !important;
    }

    /* Feedback Area */
    .feedback-section {
        background-color: #f1f5f9;
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 4px solid #1e40af;
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
            json={"model": model, "messages": messages, "max_tokens": 250}
        )
        return res.json()['choices'][0]['message']['content']
    except Exception as e:
        return f"Error: {str(e)}"

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/graduation-cap.png", width=80)
    st.title("TeacherHub")
    st.markdown("*Business English Division*")
    st.markdown("---")
    
    selected_scenario_name = st.selectbox("Current Unit:", list(SCENARIOS.keys()))
    current = SCENARIOS[selected_scenario_name]
    
    st.markdown("### ⚙️ Settings")
    if st.button("Reset Session"):
        st.session_state.messages = [
            {"role": "system", "content": f"{current['system_prompt']} Keep answers professional and educational."},
            {"role": "assistant", "content": current['start_msg']}
        ]
        st.rerun()

# --- MAIN UI ---
st.title("Telephoning Practice Environment")

col1, col2 = st.columns([1, 1.5])

with col1:
    # Instruction Card
    st.markdown(f"""
    <div class="instruction-card">
        <div class="instruction-header">Assignment Briefing</div>
        <div class="instruction-body">{current["task"]}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Vocabulary Section
    st.markdown("### 📘 Key Terminology")
    vocab_html = "".join([f'<span class="vocab-tag">{word}</span>' for word in current['vocab']])
    st.markdown(vocab_html, unsafe_allow_html=True)

with col2:
    # --- CHAT INITIALIZATION ---
    if "messages" not in st.session_state or st.session_state.get('last_scenario') != selected_scenario_name:
        st.session_state.messages = [
            {"role": "system", "content": f"{current['system_prompt']} Keep answers professional and educational."},
            {"role": "assistant", "content": current['start_msg']}
        ]
        st.session_state.last_scenario = selected_scenario_name

    # --- CHAT INTERFACE ---
    chat_container = st.container(height=550)
    with chat_container:
        for msg in st.session_state.messages[1:]:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

    # --- INPUT ---
    if prompt := st.chat_input("Compose your response..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with chat_container:
            with st.chat_message("user"):
                st.write(prompt)
            
            with st.chat_message("assistant"):
                with st.spinner("Analyzing and responding..."):
                    response = get_completion(st.session_state.messages)
                    st.write(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})

# --- FEEDBACK ---
st.markdown("---")
if st.button("📝 Generate Academic Feedback"):
    student_msgs = [m['content'] for m in st.session_state.messages if m['role'] == 'user']
    if not student_msgs:
        st.warning("Please engage in the conversation first to receive feedback.")
    else:
        with st.spinner("Reviewing conversation protocols..."):
            analysis_prompt = f"""
            Analysiere diesen Chat-Verlauf als Englischlehrer. 
            Zielgruppe: Kaufmännische Auszubildende (B1/B2).
            Sprache: DEUTSCH.
            Struktur:
            1. Stärken (Was war gut?)
            2. Vokabel-Check (Wurden {current['vocab']} genutzt?)
            3. Korrekturen (3 konkrete Beispielsätze zur Verbesserung)
            Chat-Verlauf: {student_msgs}
            """
            feedback = get_completion([{"role": "user", "content": analysis_prompt}])
            st.markdown(f'<div class="feedback-section"><h3>Educational Feedback</h3>{feedback}</div>', unsafe_allow_html=True)
