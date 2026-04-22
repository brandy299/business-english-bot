import streamlit as st
import requests
from scenarios import SCENARIOS

# --- CONFIGURATION ---
st.set_page_config(
    page_title="Business English Trainer | Academic Environment", 
    page_icon="📜", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- IMPECCABLE DESIGN SYSTEM: MODERN OXFORD ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Playfair+Display:ital,wght@0,700;1,700&display=swap');

    /* CSS Variable Definitions */
    :root {
        --primary-navy: oklch(25% 0.05 260);
        --accent-blue: oklch(45% 0.15 250);
        --surface-light: oklch(98% 0.01 250);
        --border-soft: oklch(90% 0.01 250);
        --text-main: oklch(20% 0.02 250);
        --text-muted: oklch(45% 0.02 250);
    }

    /* Base Layout Reset */
    .stApp {
        background-color: var(--surface-light);
        color: var(--text-main);
        font-family: 'Inter', sans-serif;
    }

    /* Refined Typography Hierarchy */
    h1 {
        font-family: 'Playfair Display', serif;
        font-weight: 700;
        font-size: 3.2rem !important;
        color: var(--primary-navy);
        letter-spacing: -0.02em;
        margin-bottom: 0.5rem !important;
        text-align: left;
    }

    .subtitle {
        font-family: 'Inter', sans-serif;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 0.15em;
        font-size: 0.85rem;
        font-weight: 600;
        margin-bottom: 2rem;
    }

    /* Assignment Brief - Academic Paper Style */
    .paper-surface {
        background: white;
        padding: 40px;
        border-radius: 4px;
        border: 1px solid var(--border-soft);
        box-shadow: 0 10px 30px -10px rgba(0,0,0,0.05);
        position: relative;
        overflow: hidden;
    }

    .paper-surface::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 4px;
        height: 100%;
        background: var(--primary-navy);
    }

    .section-label {
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        font-size: 0.75rem;
        color: var(--accent-blue);
        text-transform: uppercase;
        margin-bottom: 12px;
        display: block;
    }

    .brief-text {
        font-family: 'Georgia', serif;
        font-size: 1.25rem;
        line-height: 1.8;
        color: var(--text-main);
    }

    /* Vocabulary Mastery Tags */
    .vocab-grid {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        margin-top: 24px;
    }

    .vocab-item {
        background: oklch(95% 0.02 250);
        border: 1px solid oklch(85% 0.02 250);
        color: var(--primary-navy);
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 500;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .vocab-item:hover {
        background: var(--primary-navy);
        color: white;
    }

    /* Sophisticated Chat Interface */
    [data-testid="stChatMessage"] {
        background-color: transparent !important;
        border-bottom: 1px solid var(--border-soft) !important;
        border-radius: 0 !important;
        padding: 24px 0 !important;
    }

    [data-testid="stChatMessage"] p {
        font-size: 1.05rem !important;
        line-height: 1.6 !important;
    }

    /* Professional Sidebar */
    section[data-testid="stSidebar"] {
        background-color: white !important;
        border-right: 1px solid var(--border-soft);
    }

    .sidebar-header {
        font-family: 'Playfair Display', serif;
        font-size: 1.8rem;
        color: var(--primary-navy);
        padding: 20px 0;
    }

    /* Buttons - Precision Engineered */
    .stButton>button {
        background-color: var(--primary-navy) !important;
        color: white !important;
        border-radius: 2px !important;
        padding: 12px 24px !important;
        font-weight: 500 !important;
        font-size: 0.9rem !important;
        border: none !important;
        transition: all 0.3s ease !important;
        width: 100%;
    }

    .stButton>button:hover {
        background-color: var(--accent-blue) !important;
        transform: translateY(-1px);
    }

    /* Feedback Protocol */
    .feedback-protocol {
        background-color: oklch(96% 0.01 250);
        border: 1px dashed var(--border-soft);
        padding: 30px;
        margin-top: 40px;
        border-radius: 4px;
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
            json={"model": model, "messages": messages, "max_tokens": 400}
        )
        return res.json()['choices'][0]['message']['content']
    except Exception as e:
        return f"System Error: {str(e)}"

# --- SIDEBAR LOGIC ---
with st.sidebar:
    st.markdown('<div class="sidebar-header">TeacherHub</div>', unsafe_allow_html=True)
    st.markdown("---")
    
    st.markdown('<span class="section-label">Selected Curriculum</span>', unsafe_allow_html=True)
    selected_scenario_name = st.selectbox("", list(SCENARIOS.keys()), label_visibility="collapsed")
    current = SCENARIOS[selected_scenario_name]
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown('<span class="section-label">Session Controls</span>', unsafe_allow_html=True)
    if st.button("INITIALIZE SIMULATION"):
        st.session_state.messages = [
            {"role": "system", "content": f"{current['system_prompt']} Maintain a high-stakes professional tone."},
            {"role": "assistant", "content": current['start_msg']}
        ]
        st.rerun()

# --- MAIN PAGE ARCHITECTURE ---
st.markdown("<h1>Business Telephoning Simulator</h1>", unsafe_allow_html=True)
st.markdown('<div class="subtitle">Kaufmännisches Berufskolleg NRW | Advanced Business English</div>', unsafe_allow_html=True)

layout_col_left, layout_col_right = st.columns([1, 1.4], gap="large")

with layout_col_left:
    # Assignment Card
    st.markdown(f"""
    <div class="paper-surface">
        <span class="section-label">Assignment Briefing</span>
        <div class="brief-text">{current["task"]}</div>
        <br>
        <span class="section-label">Mastery Vocabulary</span>
        <div class="vocab-grid">
            {" ".join([f'<div class="vocab-item">{w}</div>' for w in current['vocab']])}
        </div>
    </div>
    """, unsafe_allow_html=True)

with layout_col_right:
    # Chat Initialization
    if "messages" not in st.session_state or st.session_state.get('last_scenario') != selected_scenario_name:
        st.session_state.messages = [
            {"role": "system", "content": f"{current['system_prompt']} Maintain a high-stakes professional tone."},
            {"role": "assistant", "content": current['start_msg']}
        ]
        st.session_state.last_scenario = selected_scenario_name

    # Chat Container
    chat_box = st.container(height=600, border=False)
    with chat_box:
        for msg in st.session_state.messages[1:]:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

    # User Input
    if prompt := st.chat_input("Compose professional response..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with chat_box:
            with st.chat_message("user"):
                st.markdown(prompt)
            with st.chat_message("assistant"):
                with st.spinner("Analyzing protocol..."):
                    response = get_completion(st.session_state.messages)
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})

# --- ANALYSIS SECTION ---
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown('<span class="section-label">Evaluation Engine</span>', unsafe_allow_html=True)
if st.button("GENERATE PERFORMANCE ANALYTICS"):
    student_msgs = [m['content'] for m in st.session_state.messages if m['role'] == 'user']
    if not student_msgs:
        st.warning("Please initiate a dialogue first.")
    else:
        with st.spinner("Compiling academic report..."):
            analysis_prompt = f"Analysiere diesen kaufmännischen Chat-Verlauf auf Deutsch (Feedback zu Höflichkeit, Vokabeln {current['vocab']}, Korrektur-Sätze): {student_msgs}"
            feedback = get_completion([{"role": "user", "content": analysis_prompt}])
            st.markdown(f'<div class="feedback-protocol"><h3>Academic Assessment Report</h3>{feedback}</div>', unsafe_allow_html=True)
