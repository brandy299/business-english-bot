import streamlit as st
import requests
from scenarios import SCENARIOS

# --- CONFIGURATION ---
st.set_page_config(
    page_title="Business Communication Lab", 
    page_icon="📞", 
    layout="wide"
)

# --- GLOBAL STYLING ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Crimson+Pro:wght@700&family=Plus+Jakarta+Sans:wght@400;600&display=swap');

    .stApp {
        background-color: #ede7de !important;
        color: #2d2d2d;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    .app-header {
        text-align: left;
        padding: 20px 0 30px 0;
        border-bottom: 2px solid #7c2d12;
        margin-bottom: 20px;
    }
    .main-title {
        font-family: 'Crimson Pro', serif;
        font-size: 3rem;
        color: #7c2d12;
        margin: 0;
        text-shadow: 0 0 10px rgba(124, 45, 18, 0.1);
    }
    .sub-tag {
        font-weight: bold;
        color: #9a3412;
        letter-spacing: 0.2em;
        font-size: 0.8rem;
        text-transform: uppercase;
    }

    /* Neon/Glow Elements */
    .active-connection-header {
        background: linear-gradient(90deg, #7c2d12, #9a3412);
        color: white;
        padding: 10px 15px;
        font-size: 0.85rem;
        font-weight: bold;
        letter-spacing: 2px;
        border-radius: 8px 8px 0 0;
        box-shadow: 0 0 15px rgba(124, 45, 18, 0.4);
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .glow-dot {
        width: 10px;
        height: 10px;
        background-color: #4ade80;
        border-radius: 50%;
        box-shadow: 0 0 8px #4ade80;
        display: inline-block;
        margin-right: 8px;
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.4; }
        100% { opacity: 1; }
    }

    .assignment-container {
        background: #ffffff;
        padding: 25px;
        border-radius: 4px;
        border: 1px solid #d1ccc1;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        margin-bottom: 25px;
    }

    .identity-card {
        background: #f8fafc;
        border-left: 4px solid #475569;
        padding: 15px;
        margin-bottom: 20px;
        font-size: 0.95rem;
    }

    .vocab-container {
        display: flex;
        flex-direction: column;
        gap: 8px;
        margin-top: 15px;
    }
    .v-row {
        display: flex;
        justify-content: space-between;
        background: #fdf6e3;
        padding: 8px 12px;
        border-radius: 4px;
        border: 1px solid #fee2e2;
        font-size: 0.9rem;
        transition: all 0.2s;
    }
    .v-row:hover {
        transform: translateX(5px);
        border-color: #7c2d12;
    }
    .v-eng { font-weight: bold; color: #7c2d12; }
    .v-ger { color: #475569; font-style: italic; }

    .stButton>button {
        background-color: #7c2d12 !important;
        color: #ffffff !important;
        border: none !important;
        padding: 12px 20px !important;
        border-radius: 4px !important;
        font-weight: bold !important;
        width: 100%;
        letter-spacing: 1px;
        transition: 0.3s;
    }
    .stButton>button:hover {
        box-shadow: 0 0 15px rgba(124, 45, 18, 0.4) !important;
        transform: translateY(-2px);
    }

    /* Chat Styling */
    .chat-master-container {
        background-color: #ffffff !important;
        border: 2px solid #d1ccc1;
        border-radius: 0 0 8px 8px;
        height: 500px;
        overflow-y: auto;
        padding: 25px;
        display: flex;
        flex-direction: column;
        gap: 20px;
    }
    .message-row { display: flex; gap: 15px; max-width: 92%; margin-bottom: 5px; }
    .row-bot { align-self: flex-start; flex-direction: row; }
    .row-user { align-self: flex-end; flex-direction: row-reverse; }

    .avatar {
        width: 45px; height: 45px; border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        font-size: 1.3rem; flex-shrink: 0; background-color: #ffffff !important;
    }
    .avatar-bot { border: 2px solid #7c2d12 !important; box-shadow: 0 0 10px rgba(124, 45, 18, 0.1); }
    .avatar-user { border: 2px solid #475569 !important; box-shadow: 0 0 10px rgba(71, 85, 105, 0.1); }

    .bubble { padding: 15px 20px; font-size: 1rem; line-height: 1.6; position: relative; }
    .bubble-bot { 
        background-color: #fdf6e3; 
        border-left: 5px solid #7c2d12; 
        border-radius: 0 12px 12px 12px; 
        color: #1a1a1a;
    }
    .bubble-user { 
        background-color: #f1f5f9; 
        border-right: 5px solid #475569; 
        border-radius: 12px 0 12px 12px; 
        text-align: left; 
        color: #1a1a1a;
    }
    .meta { font-size: 0.75rem; font-weight: bold; color: #94a3b8; margin-bottom: 5px; text-transform: uppercase; letter-spacing: 1px; }

    .checkpoint-tag {
        display: inline-block;
        padding: 4px 10px;
        background: #f1f5f9;
        border: 1px solid #cbd5e1;
        border-radius: 20px;
        font-size: 0.75rem;
        margin-right: 5px;
        margin-bottom: 5px;
        color: #475569;
    }
</style>
""", unsafe_allow_html=True)

# --- API HELPER ---
def get_completion(messages):
    try:
        API_KEY = st.secrets["OPENROUTER_API_KEY"]
        res = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "HTTP-Referer": "https://github.com/brandy299/business-english-bot",
                "X-Title": "Business Communication Lab"
            },
            json={
                "model": "google/gemma-4-26b-a4b-it:free",
                "messages": messages, 
                "max_tokens": 1000,
                "temperature": 0.7
            }
        )
        data = res.json()
        if 'choices' in data:
            return data['choices'][0]['message']['content']
        elif 'error' in data:
            return f"API Error: {data['error'].get('message', 'Unknown error')}"
        else:
            return f"Unexpected Response: {str(data)}"
    except Exception as e:
        return f"System Connection Error: {str(e)}"

# --- CHAT RENDERER ---
def render_chat_html(messages):
    inner_html = ""
    for msg in messages[1:]:
        is_bot = msg["role"] == "assistant"
        row_cls = "row-bot" if is_bot else "row-user"
        bub_cls = "bubble-bot" if is_bot else "bubble-user"
        ava_cls = "avatar-bot" if is_bot else "avatar-user"
        ava_icon = "💼" if is_bot else "🎓"
        lbl = "Business Partner" if is_bot else "Student"
        inner_html += f'<div class="message-row {row_cls}"><div class="avatar {ava_cls}">{ava_icon}</div><div style="display: flex; flex-direction: column;"><div class="meta">{lbl}</div><div class="bubble {bub_cls}">{msg["content"]}</div></div></div>'
    
    chat_container = f'<div class="chat-master-container" id="chat-box">{inner_html}</div>'
    scroll_script = '<script>var b=document.getElementById("chat-box"); if(b){b.scrollTop=b.scrollHeight;}</script>'
    return chat_container + scroll_script

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("<h2 style='color: #7c2d12; margin-top:0;'>Control Panel</h2>", unsafe_allow_html=True)
    selected_scenario_name = st.selectbox("Select Scenario", list(SCENARIOS.keys()))
    current = SCENARIOS[selected_scenario_name]
    
    st.markdown("---")
    st.markdown("### Learning Objectives")
    for cp in current['checkpoints']:
        st.markdown(f"✅ {cp}")
    
    st.markdown("---")
    if st.button("New Call", use_container_width=True):
        st.session_state.messages = [{"role": "system", "content": current['system_prompt']}, {"role": "assistant", "content": current['start_msg']}]
        st.session_state.last_scenario = selected_scenario_name
        st.rerun()

# --- MAIN PAGE ---
st.markdown(f"<div class='app-header'><div class='sub-tag'>Professional Business English</div><h1 class='main-title'>Communication Lab</h1></div>", unsafe_allow_html=True)

col_left, col_right = st.columns([1, 1.4], gap="large")

with col_left:
    # User Identity Card
    st.markdown(f"""
    <div class="identity-card">
        <div class='sub-tag' style='font-size:0.7rem;'>Your Identity</div>
        <div style="margin-top:5px;">
            <b>Company:</b> {current['user_identity']['company']}<br>
            <b>Your Role:</b> {current['user_identity']['role']}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Assignment Card
    st.markdown(f"""
    <div class="assignment-container">
        <div class='sub-tag' style='margin-bottom:10px;'>Current Mission</div>
        <div style="font-family: Georgia, serif; font-size: 1.1rem; line-height: 1.6; white-space: pre-line;">{current["task"].strip()}</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### Vocabulary Bank")
    vocab_html = '<div class="vocab-container">'
    for eng, ger in current['vocab'].items():
        vocab_html += f'<div class="v-row"><span class="v-eng">{eng}</span><span class="v-ger">{ger}</span></div>'
    vocab_html += '</div>'
    st.markdown(vocab_html, unsafe_allow_html=True)

with col_right:
    if "messages" not in st.session_state or st.session_state.get('last_scenario') != selected_scenario_name:
        st.session_state.messages = [{"role": "system", "content": current['system_prompt']}, {"role": "assistant", "content": current['start_msg']}]
        st.session_state.last_scenario = selected_scenario_name

    # Header with Neon Glow
    st.markdown(f"""
    <div class="active-connection-header">
        <span><span class="glow-dot"></span>ACTIVE CONNECTION: {current['agent_name'].upper()}</span>
        <span style="font-size: 0.7rem; opacity: 0.8;">{current['company']}</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(render_chat_html(st.session_state.messages), unsafe_allow_html=True)

    if prompt := st.chat_input("Type your response..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.spinner("Waiting for partner..."):
            response = get_completion(st.session_state.messages)
            st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()

st.markdown("<br>", unsafe_allow_html=True)
if st.button("📊 GENERATE PERFORMANCE REPORT", use_container_width=True):
    student_msgs = [m['content'] for m in st.session_state.messages if m['role'] == 'user']
    if student_msgs:
        with st.spinner("Expert AI is analyzing your performance..."):
            forbidden_list = current.get('forbidden', [])
            analysis_prompt = f"""
            You are a senior Business English teacher. Analyze this student's performance in a telephone roleplay.
            
            Scenario: {selected_scenario_name}
            Student Identity: {current['user_identity']}
            Required Checkpoints: {current['checkpoints']}
            Forbidden Phrases (deduct points if used): {forbidden_list}
            
            Structure your response as follows:
            1. **Overall Grade** (A to F)
            2. **Checkpoint Audit**: List which checkpoints were met and which were missed.
            3. **Business Etiquette**: How professional was the student? (Tone, Polite phrases like 'Could you', 'I would like')
            4. **Forbidden Phrases**: Did they use any of the forbidden words?
            5. **Key Improvements**: Give 3 specific linguistic improvements for their sentences.
            6. **Vocabulary**: Did they use the provided vocabulary?
            
            Chat History (Student only): {student_msgs}
            """
            feedback = get_completion([{"role": "user", "content": analysis_prompt}])
            st.markdown(f"""
            <div style="background:white; border-top:8px solid #7c2d12; padding:35px; border-radius:12px; box-shadow:0 15px 40px rgba(0,0,0,0.15); margin-top:30px;">
                <h2 style="color:#7c2d12; font-family:Crimson Pro; margin-top:0;">Performance Review Report</h2>
                <div style="font-size:1.05rem; line-height:1.7; color: #1e293b;">{feedback}</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("Please start a conversation before requesting a report.")
