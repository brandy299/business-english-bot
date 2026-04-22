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

# --- PROFESSIONAL ACADEMIC DESIGN (FIXED CONTRAST) ---
st.markdown("""
<style>
    /* Global Styles */
    .stApp {
        background-color: #f1f5f9; /* Helles Grau für besseren Kontrast */
        color: #0f172a;
    }

    /* Main Header */
    h1 {
        font-family: 'Georgia', serif;
        color: #1e3a8a !important;
        font-weight: 700;
        border-bottom: 2px solid #cbd5e1;
        padding-bottom: 10px;
    }

    /* Instruction Card */
    .instruction-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 8px;
        border: 1px solid #cbd5e1;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        color: #1e293b !important;
    }

    .instruction-header {
        font-family: 'Georgia', serif;
        font-weight: bold;
        color: #1e40af;
        border-bottom: 1px solid #e2e8f0;
        margin-bottom: 10px;
    }

    /* Chat Styling - FORCE VISIBILITY */
    [data-testid="stChatMessage"] {
        background-color: #ffffff !important;
        border: 1px solid #cbd5e1 !important;
        color: #0f172a !important; /* Dunkler Text */
    }
    
    /* Force text inside chat to be dark */
    [data-testid="stChatMessage"] p, [data-testid="stChatMessage"] div {
        color: #0f172a !important;
    }

    /* Sidebar Fix */
    section[data-testid="stSidebar"] {
        background-color: #ffffff !important;
    }

    /* Button Style */
    .stButton>button {
        background-color: #1e40af !important;
        color: #ffffff !important;
        border-radius: 4px;
        font-weight: bold;
    }

    /* Vocabulary Tags */
    .vocab-tag {
        display: inline-block;
        background-color: #dbeafe;
        color: #1e40af;
        padding: 4px 8px;
        border-radius: 4px;
        margin: 2px;
        font-size: 0.85rem;
        font-weight: bold;
        border: 1px solid #bfdbfe;
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
            json={"model": model, "messages": messages, "max_tokens": 300}
        )
        return res.json()['choices'][0]['message']['content']
    except Exception as e:
        return f"Error: {str(e)}"

# --- SIDEBAR ---
with st.sidebar:
    st.title("TeacherHub")
    st.markdown("---")
    selected_scenario_name = st.selectbox("Select Scenario:", list(SCENARIOS.keys()))
    current = SCENARIOS[selected_scenario_name]
    
    if st.button("Reset Chat"):
        st.session_state.messages = [
            {"role": "system", "content": f"{current['system_prompt']} Keep answers professional."},
            {"role": "assistant", "content": current['start_msg']}
        ]
        st.rerun()

# --- MAIN UI ---
st.title("Business English Trainer")

col1, col2 = st.columns([1, 2])

with col1:
    st.markdown(f"""
    <div class="instruction-card">
        <div class="instruction-header">Assignment</div>
        <div style="font-family: Georgia, serif; line-height: 1.5;">{current["task"]}</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### Vocabulary")
    vocab_html = "".join([f'<span class="vocab-tag">{word}</span>' for word in current['vocab']])
    st.markdown(vocab_html, unsafe_allow_html=True)

with col2:
    if "messages" not in st.session_state or st.session_state.get('last_scenario') != selected_scenario_name:
        st.session_state.messages = [
            {"role": "system", "content": f"{current['system_prompt']} Keep answers professional."},
            {"role": "assistant", "content": current['start_msg']}
        ]
        st.session_state.last_scenario = selected_scenario_name

    chat_container = st.container(height=500)
    with chat_container:
        for msg in st.session_state.messages[1:]:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

    if prompt := st.chat_input("Type here..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with chat_container:
            with st.chat_message("user"):
                st.write(prompt)
            with st.chat_message("assistant"):
                response = get_completion(st.session_state.messages)
                st.write(response)
                st.session_state.messages.append({"role": "assistant", "content": response})

st.divider()
if st.button("📊 Analyze Conversation"):
    student_msgs = [m['content'] for m in st.session_state.messages if m['role'] == 'user']
    if student_msgs:
        with st.spinner("Analyzing..."):
            analysis_prompt = f"Analysiere diesen Business English Chat auf Deutsch (Stärken, Vokabeln {current['vocab']}, Korrekturen): {student_msgs}"
            feedback = get_completion([{"role": "user", "content": analysis_prompt}])
            st.info(feedback)
