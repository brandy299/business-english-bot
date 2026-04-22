import streamlit as st
import requests
from scenarios import SCENARIOS

# --- CONFIGURATION ---
st.set_page_config(
    page_title="Business English | Coach", 
    page_icon="🎓", 
    layout="wide"
)

# --- CONTRAST-FOCUSED WARM ACADEMIC DESIGN ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Crimson+Pro:wght@700&family=Plus+Jakarta+Sans:wght@400;600&display=swap');

    /* Background: Clear Warm Stone (Distinct from white) */
    .stApp {
        background-color: #ede7de; 
        color: #2d2d2d;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* Header Styling */
    .header-container {
        padding: 40px 0;
        text-align: center;
    }
    .main-title {
        font-family: 'Crimson Pro', serif;
        font-size: 3.5rem;
        color: #7c2d12;
        margin-bottom: 0;
    }

    /* Left Side: Assignment Paper */
    .assignment-paper {
        background: #ffffff;
        padding: 30px;
        border-radius: 8px;
        border: 1px solid #d1ccc1;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    .paper-label {
        font-size: 0.75rem;
        font-weight: 800;
        text-transform: uppercase;
        color: #9a3412;
        letter-spacing: 0.1em;
        margin-bottom: 10px;
        display: block;
    }

    /* RIGHT SIDE: THE CHATBOX (HIGH CONTRAST) */
    .chat-frame {
        background: #ffffff !important; /* Pure White */
        border: 2px solid #d1ccc1; /* Strong Border */
        border-radius: 12px;
        box-shadow: 0 15px 45px rgba(0,0,0,0.15); /* Deep Shadow for elevation */
        overflow: hidden;
    }
    
    .chat-header {
        background: #7c2d12;
        color: white;
        padding: 12px 20px;
        font-weight: bold;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    /* Message Bubbles - High Legibility */
    .msg-box {
        margin-bottom: 20px;
        display: flex;
        flex-direction: column;
    }
    .msg-bot {
        background-color: #fdf6e3; /* Warm Tint */
        border-left: 5px solid #7c2d12;
        padding: 15px;
        color: #1a1a1a;
        font-size: 1.1rem;
        border-radius: 0 8px 8px 0;
        max-width: 90%;
    }
    .msg-user {
        background-color: #f1f5f9;
        border-right: 5px solid #475569;
        padding: 15px;
        color: #1a1a1a;
        font-size: 1.1rem;
        border-radius: 8px 0 0 8px;
        max-width: 90%;
        align-self: flex-end;
        text-align: right;
    }
    .msg-meta {
        font-size: 0.7rem;
        font-weight: bold;
        color: #94a3b8;
        margin-bottom: 4px;
        text-transform: uppercase;
    }

    /* Vocabulary */
    .v-tag {
        display: inline-block;
        background: #fef2f2;
        color: #9a3412;
        padding: 4px 12px;
        border-radius: 4px;
        margin: 3px;
        font-size: 0.85rem;
        font-weight: bold;
        border: 1px solid #fee2e2;
    }

    /* Buttons */
    .stButton>button {
        background-color: #7c2d12 !important;
        color: white !important;
        border-radius: 6px !important;
        border: none !important;
        padding: 10px 20px !important;
        font-weight: bold !important;
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
    st.markdown("<h2 style='color: #7c2d12;'>English Hub</h2>", unsafe_allow_html=True)
    st.markdown("---")
    selected_scenario_name = st.selectbox("Current Unit", list(SCENARIOS.keys()))
    current = SCENARIOS[selected_scenario_name]
    
    if st.button("New Simulation", use_container_width=True):
        st.session_state.messages = [
            {"role": "system", "content": current['system_prompt']},
            {"role": "assistant", "content": current['start_msg']}
        ]
        st.rerun()

# --- MAIN UI ---
st.markdown("<div class='header-container'><h1 class='main-title'>Business English Coach</h1></div>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1.4], gap="large")

with col1:
    st.markdown(f"""
    <div class="assignment-paper">
        <span class="paper-label">Mission Briefing</span>
        <div style="font-family: Georgia, serif; font-size: 1.2rem; line-height: 1.6;">{current["task"]}</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### Vocabulary Focus")
    v_html = "".join([f'<span class="v-tag">{w}</span>' for w in current['vocab']])
    st.markdown(v_html, unsafe_allow_html=True)

with col2:
    if "messages" not in st.session_state or st.session_state.get('last_scenario') != selected_scenario_name:
        st.session_state.messages = [
            {"role": "system", "content": current['system_prompt']},
            {"role": "assistant", "content": current['start_msg']}
        ]
        st.session_state.last_scenario = selected_scenario_name

    # THE CHAT FRAME (HIGH CONTRAST)
    st.markdown('<div class="chat-frame">', unsafe_allow_html=True)
    st.markdown('<div class="chat-header"><span>💬</span> LIVE CONVERSATION</div>', unsafe_allow_html=True)
    
    chat_box = st.container(height=550, border=False)
    with chat_box:
        for msg in st.session_state.messages[1:]:
            is_bot = msg["role"] == "assistant"
            align = "flex-start" if is_bot else "flex-end"
            cls = "msg-bot" if is_bot else "msg-user"
            lbl = "Business Partner" if is_bot else "Your Response"
            
            st.markdown(f"""
            <div class="msg-box" style="align-items: {align};">
                <div class="msg-meta">{lbl}</div>
                <div class="{cls}">{msg['content']}</div>
            </div>
            """, unsafe_allow_html=True)

    # INPUT
    if prompt := st.chat_input("Enter your message..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with chat_box:
            st.markdown(f'<div class="msg-box" style="align-items: flex-end;"><div class="msg-meta">Your Response</div><div class="msg-user">{prompt}</div></div>', unsafe_allow_html=True)
            with st.spinner("Processing..."):
                response = get_completion(st.session_state.messages)
                st.markdown(f'<div class="msg-box" style="align-items: flex-start;"><div class="msg-meta">Business Partner</div><div class="msg-bot">{response}</div></div>', unsafe_allow_html=True)
                st.session_state.messages.append({"role": "assistant", "content": response})
    st.markdown('</div>', unsafe_allow_html=True)

# --- REPORT ---
st.markdown("<br>", unsafe_allow_html=True)
if st.button("📊 GENERATE EVALUATION REPORT", use_container_width=True):
    student_msgs = [m['content'] for m in st.session_state.messages if m['role'] == 'user']
    if student_msgs:
        with st.spinner("Compiling results..."):
            feedback = get_completion([{"role": "user", "content": f"Analysiere diesen kaufmännischen Chat auf Deutsch (Stärken, Vokabeln {current['vocab']}, 3 Korrekturen): {student_msgs}"}])
            st.markdown(f"""
                <div style="background: white; border-top: 5px solid #7c2d12; padding: 30px; border-radius: 8px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); margin-top: 20px;">
                    <h3 style="color: #7c2d12; font-family: Crimson Pro;">Teacher's Feedback</h3>
                    <div style="font-size: 1.1rem; line-height: 1.6;">{feedback}</div>
                </div>
            """, unsafe_allow_html=True)
