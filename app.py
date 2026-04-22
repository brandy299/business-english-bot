import streamlit as st
import requests
from scenarios import SCENARIOS

# --- CONFIGURATION ---
st.set_page_config(
    page_title="Business English Trainer", 
    page_icon="🎓", 
    layout="wide"
)

# --- ROBUST DESIGN SYSTEM (CUSTOM HTML CHAT) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&family=Georgia&display=swap');

    .stApp {
        background-color: #ffffff;
        color: #1a1a1a;
        font-family: 'Inter', sans-serif;
    }

    /* Header Styling */
    .main-title {
        font-family: 'Georgia', serif;
        font-size: 2.8rem;
        color: #1e3a8a;
        font-weight: bold;
        border-bottom: 3px solid #1e3a8a;
        padding-bottom: 10px;
        margin-bottom: 30px;
    }

    /* CUSTOM CHAT BUBBLES - NO STREAMLIT DEFAULTS */
    .chat-wrapper {
        margin-bottom: 20px;
        display: flex;
        flex-direction: column;
    }

    .msg-assistant {
        background-color: #1e3a8a;
        color: #ffffff !important;
        padding: 15px 20px;
        border-radius: 15px 15px 15px 0px;
        max-width: 85%;
        align-self: flex-start;
        font-size: 1.1rem;
        line-height: 1.5;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        border: 1px solid #1e3a8a;
    }

    .msg-user {
        background-color: #f1f5f9;
        color: #0f172a !important;
        padding: 15px 20px;
        border-radius: 15px 15px 0px 15px;
        max-width: 85%;
        align-self: flex-end;
        font-size: 1.1rem;
        line-height: 1.5;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
        border: 1px solid #cbd5e1;
        text-align: right;
    }

    .avatar-label {
        font-size: 0.75rem;
        font-weight: bold;
        text-transform: uppercase;
        margin-bottom: 5px;
        color: #64748b;
    }

    /* Instruction Area */
    .assignment-box {
        background-color: #f8fafc;
        border-left: 6px solid #1e3a8a;
        padding: 25px;
        border-radius: 4px;
        font-family: 'Georgia', serif;
        font-size: 1.2rem;
        color: #1e293b;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }

    /* Sidebar Fix */
    section[data-testid="stSidebar"] {
        background-color: #f1f5f9 !important;
        border-right: 2px solid #e2e8f0;
    }

    /* Vocabulary Master */
    .tag {
        display: inline-block;
        background: #1e3a8a;
        color: white;
        padding: 5px 12px;
        border-radius: 20px;
        margin: 3px;
        font-size: 0.9rem;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# --- API HELPERS ---
def get_completion(messages):
    try:
        API_KEY = st.secrets["OPENROUTER_API_KEY"]
        res = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={"Authorization": f"Bearer {API_KEY}"},
            json={"model": "meta-llama/llama-3-8b-instruct", "messages": messages, "max_tokens": 400}
        )
        return res.json()['choices'][0]['message']['content']
    except Exception as e:
        return f"Simulation Error: {str(e)}"

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("## 🎓 TeacherHub")
    st.markdown("---")
    selected_scenario_name = st.selectbox("Current Module:", list(SCENARIOS.keys()))
    current = SCENARIOS[selected_scenario_name]
    
    if st.button("RESET SIMULATION", use_container_width=True):
        st.session_state.messages = [
            {"role": "system", "content": current['system_prompt']},
            {"role": "assistant", "content": current['start_msg']}
        ]
        st.rerun()

# --- MAIN UI ---
st.markdown(f'<div class="main-title">Business English Trainer</div>', unsafe_allow_html=True)

col1, col2 = st.columns([1, 1.3], gap="large")

with col1:
    st.markdown("### 📋 Assignment Briefing")
    st.markdown(f'<div class="assignment-box">{current["task"]}</div>', unsafe_allow_html=True)
    
    st.markdown("<br>### 📘 Key Vocabulary", unsafe_allow_html=True)
    vocab_html = "".join([f'<span class="tag">{w}</span>' for w in current['vocab']])
    st.markdown(vocab_html, unsafe_allow_html=True)

with col2:
    # Initialization
    if "messages" not in st.session_state or st.session_state.get('last_scenario') != selected_scenario_name:
        st.session_state.messages = [
            {"role": "system", "content": current['system_prompt']},
            {"role": "assistant", "content": current['start_msg']}
        ]
        st.session_state.last_scenario = selected_scenario_name

    # CUSTOM CHAT DISPLAY
    chat_container = st.container(height=550, border=False)
    with chat_container:
        for msg in st.session_state.messages[1:]:
            role_class = "msg-assistant" if msg["role"] == "assistant" else "msg-user"
            label = "🧑‍💼 Assistant" if msg["role"] == "assistant" else "👤 Student"
            
            st.markdown(f"""
            <div class="chat-wrapper">
                <div class="avatar-label">{label}</div>
                <div class="{role_class}">{msg['content']}</div>
            </div>
            """, unsafe_allow_html=True)

    # INPUT
    if prompt := st.chat_input("Compose your response..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with chat_container:
            # User Msg
            st.markdown(f'<div class="chat-wrapper"><div class="avatar-label">👤 Student</div><div class="msg-user">{prompt}</div></div>', unsafe_allow_html=True)
            
            # Bot Resp
            with st.spinner("Processing..."):
                response = get_completion(st.session_state.messages)
                st.markdown(f'<div class="chat-wrapper"><div class="avatar-label">🧑‍💼 Assistant</div><div class="msg-assistant">{response}</div></div>', unsafe_allow_html=True)
                st.session_state.messages.append({"role": "assistant", "content": response})

# --- FEEDBACK ---
st.markdown("---")
if st.button("📊 GENERATE EVALUATION REPORT"):
    student_msgs = [m['content'] for m in st.session_state.messages if m['role'] == 'user']
    if student_msgs:
        with st.spinner("Analyzing..."):
            analysis_prompt = f"Analysiere diesen kaufmännischen Chat auf Deutsch (Feedback zu Höflichkeit, Vokabeln {current['vocab']}, 3 Korrektur-Sätze): {student_msgs}"
            feedback = get_completion([{"role": "user", "content": analysis_prompt}])
            st.success("### 📝 Performance Evaluation")
            st.markdown(feedback)
