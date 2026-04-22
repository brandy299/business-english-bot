import streamlit as st
import requests
from scenarios import SCENARIOS

# --- CONFIGURATION ---
st.set_page_config(
    page_title="Business English Trainer | Pro", 
    page_icon="🎓", 
    layout="wide"
)

# --- IMPECCABLE DARK ACADEMIC DESIGN ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&family=Playfair+Display:ital,wght@0,700;1,700&display=swap');

    /* Global Reset */
    .stApp {
        background-color: #020617; /* Deepest Navy */
        color: #f1f5f9;
        font-family: 'Inter', sans-serif;
    }

    /* Main Title Section */
    .title-container {
        padding: 40px 0;
        text-align: center;
        background: linear-gradient(180deg, rgba(30, 58, 138, 0.2) 0%, rgba(2, 6, 23, 0) 100%);
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        margin-bottom: 40px;
    }
    
    .main-title {
        font-family: 'Playfair Display', serif;
        font-size: 3.5rem;
        background: linear-gradient(to right, #ffffff, #94a3b8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
    }

    /* Assignment Card - Dark Paper Style */
    .assignment-card {
        background: rgba(30, 41, 59, 0.5);
        backdrop-filter: blur(10px);
        padding: 30px;
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 20px 50px rgba(0,0,0,0.3);
    }

    .section-label {
        color: #38bdf8; /* Electric Blue Accent */
        text-transform: uppercase;
        letter-spacing: 0.1em;
        font-size: 0.75rem;
        font-weight: 600;
        margin-bottom: 15px;
        display: block;
    }

    .brief-text {
        font-family: 'Georgia', serif;
        font-size: 1.25rem;
        line-height: 1.8;
        color: #e2e8f0;
    }

    /* Glassmorphism Chat Container */
    .chat-interface {
        background: rgba(15, 23, 42, 0.8);
        border: 1px solid rgba(56, 189, 248, 0.2);
        border-radius: 24px;
        padding: 20px;
        box-shadow: 0 0 40px rgba(0,0,0,0.5), inset 0 0 20px rgba(56, 189, 248, 0.05);
    }

    /* Custom Message Bubbles */
    .message-row {
        margin-bottom: 24px;
        display: flex;
        flex-direction: column;
    }

    .assistant-bubble {
        background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 100%);
        color: white;
        padding: 18px 22px;
        border-radius: 20px 20px 20px 4px;
        max-width: 85%;
        align-self: flex-start;
        border: 1px solid rgba(255, 255, 255, 0.1);
        font-size: 1.05rem;
        line-height: 1.6;
    }

    .user-bubble {
        background: rgba(51, 65, 85, 0.5);
        color: #f1f5f9;
        padding: 18px 22px;
        border-radius: 20px 20px 4px 20px;
        max-width: 85%;
        align-self: flex-end;
        border: 1px solid rgba(255, 255, 255, 0.05);
        font-size: 1.05rem;
        line-height: 1.6;
    }

    .bubble-meta {
        font-size: 0.7rem;
        text-transform: uppercase;
        color: #64748b;
        margin-bottom: 6px;
        font-weight: 600;
    }

    /* Vocabulary Tags */
    .tag {
        display: inline-block;
        background: rgba(56, 189, 248, 0.1);
        color: #38bdf8;
        padding: 6px 14px;
        border-radius: 30px;
        margin: 4px;
        font-size: 0.85rem;
        font-weight: 600;
        border: 1px solid rgba(56, 189, 248, 0.2);
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #020617 !important;
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }

    /* Buttons */
    .stButton>button {
        background: #38bdf8 !important;
        color: #020617 !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        padding: 12px 24px !important;
        transition: 0.3s all ease;
    }
    
    .stButton>button:hover {
        background: #7dd3fc !important;
        box-shadow: 0 0 20px rgba(56, 189, 248, 0.4);
        transform: translateY(-2px);
    }

    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    ::-webkit-scrollbar-thumb {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
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
        return f"Error: {str(e)}"

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("<br><h2 style='color: white;'>TeacherHub</h2>", unsafe_allow_html=True)
    st.markdown("---")
    selected_scenario_name = st.selectbox("Curriculum Module", list(SCENARIOS.keys()))
    current = SCENARIOS[selected_scenario_name]
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("RESET SIMULATION", use_container_width=True):
        st.session_state.messages = [
            {"role": "system", "content": current['system_prompt']},
            {"role": "assistant", "content": current['start_msg']}
        ]
        st.rerun()

# --- MAIN UI ---
st.markdown("""
    <div class='title-container'>
        <div class='main-title'>Business English Pro</div>
        <p style='color: #64748b; letter-spacing: 0.2em; font-size: 0.9rem;'>KAUFMÄNNISCHES BERUFSKOLLEG NRW</p>
    </div>
""", unsafe_allow_html=True)

col_left, col_right = st.columns([1, 1.4], gap="large")

with col_left:
    st.markdown(f"""
    <div class="assignment-card">
        <span class="section-label">Mission Briefing</span>
        <div class="brief-text">{current["task"]}</div>
        <br>
        <span class="section-label">Required Terminology</span>
        <div>{" ".join([f'<span class="tag">{w}</span>' for w in current['vocab']])}</div>
    </div>
    """, unsafe_allow_html=True)

with col_right:
    # Initialization
    if "messages" not in st.session_state or st.session_state.get('last_scenario') != selected_scenario_name:
        st.session_state.messages = [
            {"role": "system", "content": current['system_prompt']},
            {"role": "assistant", "content": current['start_msg']}
        ]
        st.session_state.last_scenario = selected_scenario_name

    # CUSTOM CHAT BOX
    st.markdown('<div class="chat-interface">', unsafe_allow_html=True)
    chat_box = st.container(height=550, border=False)
    with chat_box:
        for msg in st.session_state.messages[1:]:
            is_bot = msg["role"] == "assistant"
            cls = "assistant-bubble" if is_bot else "user-bubble"
            lbl = "BUSINESS PARTNER" if is_bot else "STUDENT"
            align = "flex-start" if is_bot else "flex-end"
            
            st.markdown(f"""
            <div class="message-row" style="align-items: {align};">
                <div class="bubble-meta">{lbl}</div>
                <div class="{cls}">{msg['content']}</div>
            </div>
            """, unsafe_allow_html=True)

    # INPUT
    if prompt := st.chat_input("Enter your message..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with chat_box:
            st.markdown(f'<div class="message-row" style="align-items: flex-end;"><div class="bubble-meta">STUDENT</div><div class="user-bubble">{prompt}</div></div>', unsafe_allow_html=True)
            
            with st.spinner("Processing protocol..."):
                response = get_completion(st.session_state.messages)
                st.markdown(f'<div class="message-row" style="align-items: flex-start;"><div class="bubble-meta">BUSINESS PARTNER</div><div class="assistant-bubble">{response}</div></div>', unsafe_allow_html=True)
                st.session_state.messages.append({"role": "assistant", "content": response})
    st.markdown('</div>', unsafe_allow_html=True)

# --- FEEDBACK ---
st.markdown("<br><br>", unsafe_allow_html=True)
if st.button("📊 GENERATE ANALYTICS REPORT", use_container_width=True):
    student_msgs = [m['content'] for m in st.session_state.messages if m['role'] == 'user']
    if student_msgs:
        with st.spinner("Compiling academic data..."):
            feedback = get_completion([{"role": "user", "content": f"Analysiere diesen kaufmännischen Chat auf Deutsch (Stärken, Vokabeln {current['vocab']}, 3 Korrekturen): {student_msgs}"}])
            st.markdown(f"""
                <div style="background: rgba(30, 41, 59, 0.8); border: 1px solid #38bdf8; padding: 30px; border-radius: 16px; margin-top: 20px;">
                    <h3 style="color: #38bdf8; margin-top: 0;">Performance Report</h3>
                    <div style="color: #e2e8f0; line-height: 1.6;">{feedback}</div>
                </div>
            """, unsafe_allow_html=True)
