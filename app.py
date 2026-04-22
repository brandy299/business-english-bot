import streamlit as st
import requests
from scenarios import SCENARIOS

# --- CONFIGURATION ---
st.set_page_config(
    page_title="Business English | Editorial", 
    page_icon="✒️", 
    layout="wide"
)

# --- EDITORIAL NOIR DESIGN (BEYOND GENERIC) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Bodoni+Moda:ital,wght@0,400;0,700;1,400&family=Inter:wght@300;400;600&display=swap');

    /* Atmospheric Background with Gradient Mesh & Noise */
    .stApp {
        background: 
            radial-gradient(circle at 10% 20%, rgba(30, 41, 59, 0.4) 0%, transparent 40%),
            radial-gradient(circle at 90% 80%, rgba(15, 23, 42, 0.4) 0%, transparent 40%),
            linear-gradient(135deg, #020617 0%, #0f172a 100%);
        background-attachment: fixed;
        color: #f1f5f9;
        font-family: 'Inter', sans-serif;
    }

    /* Noise Texture Overlay */
    .stApp::before {
        content: "";
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        background-image: url('https://grainy-gradients.vercel.app/noise.svg');
        opacity: 0.05;
        pointer-events: none;
        z-index: 0;
    }

    /* Editorial Header */
    .editorial-header {
        padding: 60px 0;
        text-align: left;
        max-width: 1200px;
        margin: 0 auto;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    }

    .editorial-title {
        font-family: 'Bodoni Moda', serif;
        font-size: 5rem;
        font-weight: 700;
        letter-spacing: -0.03em;
        line-height: 0.9;
        margin-bottom: 20px;
        color: #ffffff;
    }

    .editorial-meta {
        text-transform: uppercase;
        letter-spacing: 0.3em;
        font-size: 0.8rem;
        color: #64748b;
        font-weight: 600;
    }

    /* Asymmetric Layout Cards */
    .assignment-block {
        background: rgba(255, 255, 255, 0.02);
        backdrop-filter: blur(20px);
        padding: 40px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-top: 4px solid #ffffff; /* Sharp Contrast */
        margin-top: -30px; /* Grid Breaking */
        box-shadow: 0 30px 60px rgba(0,0,0,0.4);
    }

    .brief-label {
        font-family: 'Bodoni Moda', serif;
        font-style: italic;
        font-size: 1.5rem;
        color: #94a3b8;
        margin-bottom: 20px;
        display: block;
    }

    .brief-content {
        font-family: 'Bodoni Moda', serif;
        font-size: 1.4rem;
        line-height: 1.6;
        color: #e2e8f0;
    }

    /* Floating Chat Interface */
    .chat-card {
        background: rgba(0, 0, 0, 0.3);
        border-radius: 0; /* Brutalist sharp edges */
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 20px;
        box-shadow: 0 40px 100px rgba(0,0,0,0.6);
    }

    /* Distinctive Message Bubbles */
    .msg-wrapper {
        margin-bottom: 30px;
        padding-bottom: 15px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.03);
    }

    .msg-role {
        font-size: 0.7rem;
        text-transform: uppercase;
        letter-spacing: 0.2em;
        color: #64748b;
        margin-bottom: 10px;
    }

    .msg-text-bot {
        font-size: 1.2rem;
        color: #ffffff;
        line-height: 1.6;
    }

    .msg-text-user {
        font-size: 1.2rem;
        color: #94a3b8;
        font-style: italic;
    }

    /* Vocabulary Masterpiece */
    .vocab-strip {
        display: flex;
        gap: 15px;
        overflow-x: auto;
        padding: 10px 0;
        margin-top: 20px;
    }

    .vocab-tag {
        font-size: 0.8rem;
        text-transform: uppercase;
        padding: 5px 15px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        color: #ffffff;
        white-space: nowrap;
    }

    /* Sidebar Reset */
    section[data-testid="stSidebar"] {
        background-color: #020617 !important;
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }

    /* Primary Button - Pure Luxury */
    .stButton>button {
        background: transparent !important;
        color: white !important;
        border: 1px solid white !important;
        border-radius: 0 !important;
        text-transform: uppercase;
        letter-spacing: 0.2em;
        padding: 15px 30px !important;
        transition: 0.4s;
    }

    .stButton>button:hover {
        background: white !important;
        color: black !important;
        box-shadow: 0 0 30px rgba(255, 255, 255, 0.2);
    }

    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- API HELPERS ---
def get_completion(messages):
    try:
        API_KEY = st.secrets["OPENROUTER_API_KEY"]
        res = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={"Authorization": f"Bearer {API_KEY}"},
            json={"model": "meta-llama/llama-3-8b-instruct", "messages": messages, "max_tokens": 500}
        )
        return res.json()['choices'][0]['message']['content']
    except Exception as e:
        return f"System Error: {str(e)}"

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("<h2 style='font-family: Bodoni Moda; color: white;'>The Coach.</h2>", unsafe_allow_html=True)
    st.markdown("---")
    selected_scenario_name = st.selectbox("Current Selection", list(SCENARIOS.keys()))
    current = SCENARIOS[selected_scenario_name]
    
    if st.button("New Protocol", use_container_width=True):
        st.session_state.messages = [
            {"role": "system", "content": current['system_prompt']},
            {"role": "assistant", "content": current['start_msg']}
        ]
        st.rerun()

# --- MAIN UI ---
st.markdown("""
    <div class='editorial-header'>
        <div class='editorial-meta'>Educational Protocol // Issue 01</div>
        <div class='editorial-title'>Professional<br>Communication.</div>
    </div>
""", unsafe_allow_html=True)

col_left, col_right = st.columns([1, 1.2], gap="large")

with col_left:
    st.markdown(f"""
    <div class="assignment-block">
        <span class="brief-label">The Assignment.</span>
        <div class="brief-content">{current["task"]}</div>
        <div class="vocab-strip">
            {" ".join([f'<span class="vocab-tag">{w}</span>' for w in current['vocab']])}
        </div>
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
    st.markdown('<div class="chat-card">', unsafe_allow_html=True)
    chat_box = st.container(height=500, border=False)
    with chat_box:
        for msg in st.session_state.messages[1:]:
            is_bot = msg["role"] == "assistant"
            role_text = "Business Partner" if is_bot else "Student / Response"
            txt_class = "msg-text-bot" if is_bot else "msg-text-user"
            
            st.markdown(f"""
            <div class="msg-wrapper">
                <div class="msg-role">{role_text}</div>
                <div class="{txt_class}">{msg['content']}</div>
            </div>
            """, unsafe_allow_html=True)

    # INPUT
    if prompt := st.chat_input("Compose..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with chat_box:
            st.markdown(f'<div class="msg-wrapper"><div class="msg-role">Student / Response</div><div class="msg-text-user">{prompt}</div></div>', unsafe_allow_html=True)
            
            with st.spinner("Analyzing..."):
                response = get_completion(st.session_state.messages)
                st.markdown(f'<div class="msg-wrapper"><div class="msg-role">Business Partner</div><div class="msg-text-bot">{response}</div></div>', unsafe_allow_html=True)
                st.session_state.messages.append({"role": "assistant", "content": response})
    st.markdown('</div>', unsafe_allow_html=True)

# --- ANALYTICS ---
st.markdown("<br><br>", unsafe_allow_html=True)
if st.button("Generate Performance Analytics", use_container_width=True):
    student_msgs = [m['content'] for m in st.session_state.messages if m['role'] == 'user']
    if student_msgs:
        with st.spinner("Compiling..."):
            feedback = get_completion([{"role": "user", "content": f"Analysiere diesen Chat auf Deutsch (Stärken, Vokabeln {current['vocab']}, 3 Korrekturen): {student_msgs}"}])
            st.markdown(f"""
                <div style="background: white; color: black; padding: 50px; margin-top: 40px; box-shadow: 0 50px 100px rgba(0,0,0,0.5);">
                    <h2 style="font-family: Bodoni Moda; border-bottom: 2px solid black; padding-bottom: 20px;">Review Report.</h2>
                    <div style="font-size: 1.2rem; line-height: 1.7;">{feedback}</div>
                </div>
            """, unsafe_allow_html=True)
