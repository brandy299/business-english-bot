import streamlit as st
import requests
from scenarios import SCENARIOS

# --- CONFIGURATION ---
st.set_page_config(
    page_title="Business English | Learning Canvas", 
    page_icon="📖", 
    layout="wide"
)

# --- WARM ACADEMIC CANVAS DESIGN ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Crimson+Pro:ital,wght@0,400;0,700;1,400&family=Plus+Jakarta+Sans:wght@300;400;600&display=swap');

    /* Global Base - Warm Parchment */
    .stApp {
        background-color: #fdfaf6;
        color: #2d2d2d;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* Subtle Texture Overlay */
    .stApp::before {
        content: "";
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        background-image: url('https://www.transparenttextures.com/patterns/natural-paper.png');
        opacity: 0.4;
        pointer-events: none;
        z-index: 0;
    }

    /* Header Section */
    .header-container {
        padding: 50px 0;
        text-align: center;
    }

    .main-title {
        font-family: 'Crimson Pro', serif;
        font-size: 3.8rem;
        font-weight: 700;
        color: #7c2d12; /* Warm Terracotta */
        margin-bottom: 5px;
        letter-spacing: -0.02em;
    }

    .sub-title {
        text-transform: uppercase;
        letter-spacing: 0.2em;
        font-size: 0.85rem;
        color: #9a3412;
        font-weight: 600;
    }

    /* Assignment Section - High Quality Stationery Style */
    .assignment-card {
        background: #ffffff;
        padding: 35px;
        border-radius: 4px;
        border-top: 5px solid #7c2d12;
        box-shadow: 0 10px 25px rgba(0,0,0,0.03);
        margin-bottom: 30px;
    }

    .section-label {
        font-family: 'Plus Jakarta Sans', sans-serif;
        text-transform: uppercase;
        font-size: 0.75rem;
        font-weight: 700;
        color: #9a3412;
        margin-bottom: 15px;
        display: block;
    }

    .assignment-text {
        font-family: 'Georgia', serif;
        font-size: 1.3rem;
        line-height: 1.7;
        color: #374151;
    }

    /* THE CHATBOX - Distinct Elevation */
    .chat-container {
        background: #ffffff;
        border-radius: 12px;
        padding: 25px;
        box-shadow: 0 20px 50px rgba(0,0,0,0.06), 0 0 0 1px rgba(0,0,0,0.02);
        border: 1px solid #f3f4f6;
    }

    /* Message Bubbles */
    .message-bubble-bot {
        background-color: #fefce8; /* Very soft warm yellow tint */
        border-left: 4px solid #ca8a04;
        padding: 15px 20px;
        margin-bottom: 20px;
        border-radius: 0 8px 8px 0;
        font-size: 1.1rem;
        line-height: 1.5;
        color: #1f2937;
    }

    .message-bubble-user {
        background-color: #f8fafc;
        border-right: 4px solid #64748b;
        padding: 15px 20px;
        margin-bottom: 20px;
        border-radius: 8px 0 0 8px;
        font-size: 1.1rem;
        line-height: 1.5;
        color: #1f2937;
        text-align: right;
    }

    .role-label {
        font-size: 0.7rem;
        font-weight: 700;
        text-transform: uppercase;
        color: #9ca3af;
        margin-bottom: 5px;
    }

    /* Vocabulary Master List */
    .vocab-tag {
        display: inline-block;
        background: #fff7ed;
        color: #9a3412;
        padding: 6px 14px;
        border-radius: 6px;
        margin: 4px;
        font-size: 0.85rem;
        font-weight: 600;
        border: 1px solid #ffedd5;
    }

    /* Sidebar - Clean & Professional */
    section[data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1px solid #e5e7eb;
    }

    /* Primary Actions */
    .stButton>button {
        background-color: #7c2d12 !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 6px !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
        transition: 0.2s all ease;
    }

    .stButton>button:hover {
        background-color: #9a3412 !important;
        box-shadow: 0 4px 12px rgba(124, 45, 18, 0.2) !important;
    }

    /* Custom Scrollbar for the Canvas vibe */
    ::-webkit-scrollbar { width: 10px; }
    ::-webkit-scrollbar-track { background: #fdfaf6; }
    ::-webkit-scrollbar-thumb { background: #e5e7eb; border-radius: 5px; }
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
    st.markdown("<br><h2 style='color: #7c2d12; font-family: Crimson Pro;'>TeacherHub</h2>", unsafe_allow_html=True)
    st.markdown("---")
    selected_scenario_name = st.selectbox("Current Unit", list(SCENARIOS.keys()))
    current = SCENARIOS[selected_scenario_name]
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("New Session", use_container_width=True):
        st.session_state.messages = [
            {"role": "system", "content": current['system_prompt']},
            {"role": "assistant", "content": current['start_msg']}
        ]
        st.rerun()

# --- MAIN UI ---
st.markdown("""
    <div class='header-container'>
        <div class='main-title'>Business English Coach</div>
        <div class='sub-title'>Interactive Training Environment</div>
    </div>
""", unsafe_allow_html=True)

col_left, col_right = st.columns([1, 1.4], gap="large")

with col_left:
    st.markdown(f"""
    <div class="assignment-card">
        <span class="section-label">Your Assignment</span>
        <div class="assignment-text">{current["task"]}</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### Vocabulary Focus")
    vocab_html = "".join([f'<span class="vocab-tag">{w}</span>' for w in current['vocab']])
    st.markdown(vocab_html, unsafe_allow_html=True)

with col_right:
    # Initialization
    if "messages" not in st.session_state or st.session_state.get('last_scenario') != selected_scenario_name:
        st.session_state.messages = [
            {"role": "system", "content": current['system_prompt']},
            {"role": "assistant", "content": current['start_msg']}
        ]
        st.session_state.last_scenario = selected_scenario_name

    # THE CHAT INTERFACE
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    chat_box = st.container(height=550, border=False)
    with chat_box:
        for msg in st.session_state.messages[1:]:
            is_bot = msg["role"] == "assistant"
            bubble_cls = "message-bubble-bot" if is_bot else "message-bubble-user"
            lbl = "Business Partner" if is_bot else "Your Response"
            align = "flex-start" if is_bot else "flex-end"
            
            st.markdown(f"""
            <div style="display: flex; flex-direction: column; align-items: {align};">
                <div class="role-label">{lbl}</div>
                <div class="{bubble_cls}">{msg['content']}</div>
            </div>
            """, unsafe_allow_html=True)

    # INPUT
    if prompt := st.chat_input("Enter your message..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with chat_box:
            st.markdown(f'<div style="display: flex; flex-direction: column; align-items: flex-end;"><div class="role-label">Your Response</div><div class="message-bubble-user">{prompt}</div></div>', unsafe_allow_html=True)
            
            with st.spinner("Processing..."):
                response = get_completion(st.session_state.messages)
                st.markdown(f'<div style="display: flex; flex-direction: column; align-items: flex-start;"><div class="role-label">Business Partner</div><div class="message-bubble-bot">{response}</div></div>', unsafe_allow_html=True)
                st.session_state.messages.append({"role": "assistant", "content": response})
    st.markdown('</div>', unsafe_allow_html=True)

# --- ANALYTICS ---
st.markdown("<br><br>", unsafe_allow_html=True)
if st.button("📊 GENERATE EVALUATION REPORT", use_container_width=True):
    student_msgs = [m['content'] for m in st.session_state.messages if m['role'] == 'user']
    if student_msgs:
        with st.spinner("Compiling results..."):
            feedback = get_completion([{"role": "user", "content": f"Analysiere diesen kaufmännischen Chat auf Deutsch (Stärken, Vokabeln {current['vocab']}, 3 Korrekturen): {student_msgs}"}])
            st.markdown(f"""
                <div style="background: #ffffff; border-top: 4px solid #7c2d12; padding: 40px; border-radius: 4px; box-shadow: 0 10px 30px rgba(0,0,0,0.05);">
                    <h3 style="color: #7c2d12; font-family: Crimson Pro; font-size: 2rem;">Teacher's Feedback</h3>
                    <div style="font-size: 1.15rem; line-height: 1.7; color: #374151;">{feedback}</div>
                </div>
            """, unsafe_allow_html=True)
