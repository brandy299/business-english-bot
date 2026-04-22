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
    }
    .main-title {
        font-family: 'Crimson Pro', serif;
        font-size: 3rem;
        color: #7c2d12;
        margin: 0;
    }
    .sub-tag {
        font-weight: bold;
        color: #9a3412;
        letter-spacing: 0.1em;
        font-size: 0.8rem;
        text-transform: uppercase;
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
    }
    .v-eng { font-weight: bold; color: #7c2d12; }
    .v-ger { color: #475569; font-style: italic; }

    .stButton>button {
        background-color: #7c2d12 !important;
        color: #ffffff !important;
        border: none !important;
        padding: 10px 20px !important;
        border-radius: 4px !important;
        font-weight: bold !important;
        width: 100%;
    }

    /* Chat Styling */
    .chat-master-container {
        background-color: #ffffff !important;
        border: 2px solid #d1ccc1;
        border-radius: 0 0 8px 8px;
        height: 550px;
        overflow-y: auto;
        padding: 20px;
        display: flex;
        flex-direction: column;
        gap: 20px;
    }
    .message-row { display: flex; gap: 12px; max-width: 90%; margin-bottom: 15px; }
    .row-bot { align-self: flex-start; flex-direction: row; }
    .row-user { align-self: flex-end; flex-direction: row-reverse; }

    .avatar {
        width: 40px; height: 40px; border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        font-size: 1.2rem; flex-shrink: 0; background-color: #ffffff !important;
    }
    .avatar-bot { border: 2px solid #7c2d12 !important; }
    .avatar-user { border: 2px solid #475569 !important; }

    .bubble { padding: 12px 18px; font-size: 1rem; line-height: 1.5; }
    .bubble-bot { background-color: #fdf6e3; border-left: 4px solid #7c2d12; border-radius: 0 8px 8px 8px; color: #1a1a1a; }
    .bubble-user { background-color: #f1f5f9; border-right: 4px solid #475569; border-radius: 8px 0 8px 8px; text-align: right; color: #1a1a1a; }
    .meta { font-size: 0.7rem; font-weight: bold; color: #94a3b8; margin-bottom: 3px; text-transform: uppercase; }
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
                "HTTP-Referer": "https://github.com/brandy299/business-english-bot", # Optional but good practice
                "X-Title": "Business English Bot"
            },
            json={
                "model": "google/gemma-4-26b-a4b-it", 
                "messages": messages, 
                "max_tokens": 800
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
        lbl = "Partner" if is_bot else "You"
        inner_html += f'<div class="message-row {row_cls}"><div class="avatar {ava_cls}">{ava_icon}</div><div style="display: flex; flex-direction: column;"><div class="meta">{lbl}</div><div class="bubble {bub_cls}">{msg["content"]}</div></div></div>'
    return f'<div class="chat-master-container" id="chat-box">{inner_html}</div><script>var b=document.getElementById("chat-box");if(b){{b.scrollTop=b.scrollHeight;}}</script>'

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("<h2 style='color: #7c2d12; margin-top:0;'>Control Panel</h2>", unsafe_allow_html=True)
    selected_scenario_name = st.selectbox("Select Scenario", list(SCENARIOS.keys()))
    current = SCENARIOS[selected_scenario_name]
    st.markdown("---")
    if st.button("New Call", use_container_width=True):
        st.session_state.messages = [{"role": "system", "content": current['system_prompt']}, {"role": "assistant", "content": current['start_msg']}]
        st.rerun()

# --- MAIN PAGE ---
st.markdown(f"<div class='app-header'><div class='sub-tag'>Business English Training</div><h1 class='main-title'>Communication Lab</h1></div>", unsafe_allow_html=True)

col_left, col_right = st.columns([1, 1.4], gap="large")

with col_left:
    # User Identity Card
    st.markdown(f"""
    <div class="identity-card">
        <div class='sub-tag' style='font-size:0.7rem;'>Your Identity</div>
        <b>Company:</b> {current['user_identity']['company']}<br>
        <b>Your Role:</b> {current['user_identity']['role']}
    </div>
    """, unsafe_allow_html=True)

    # Assignment Card
    st.markdown(f"""
    <div class="assignment-container">
        <div class='sub-tag' style='margin-bottom:10px;'>Scenario Objectives</div>
        <div style="font-family: Georgia, serif; font-size: 1.15rem; line-height: 1.6; white-space: pre-line;">{current["task"].strip()}</div>
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

    st.markdown('<div style="background:#7c2d12; color:white; padding:8px 15px; font-size:0.8rem; font-weight:bold; letter-spacing:1px; border-radius: 8px 8px 0 0;">ACTIVE CONNECTION</div>', unsafe_allow_html=True)
    st.markdown(render_chat_html(st.session_state.messages), unsafe_allow_html=True)

    if prompt := st.chat_input("Speak now..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.spinner("Partner is typing..."):
            response = get_completion(st.session_state.messages)
            st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()

st.markdown("<br>", unsafe_allow_html=True)
if st.button("📊 ANALYZE CALL", use_container_width=True):
    student_msgs = [m['content'] for m in st.session_state.messages if m['role'] == 'user']
    if student_msgs:
        with st.spinner("Reviewing call logs..."):
            # Spezifisches Feedback zu den Checkpoints
            analysis_prompt = f"""
            Analysiere diesen kaufmännischen Chat auf Deutsch.
            Schüler-Identität: {current['user_identity']}
            Zwingend zu nennende Informationen (Checkpoints): {current['checkpoints']}
            Vokabeln: {list(current['vocab'].keys())}

            Bewerte:
            1. Hat der Schüler seine Firma ({current['user_identity']['company']}) genannt?
            2. Wurden ALLE Checkpoints ({current['checkpoints']}) im Gespräch erwähnt? Falls nicht, liste die fehlenden auf.
            3. Höflichkeit & kaufmännische Etikette.
            4. 3 konkrete Verbesserungsvorschläge für die englischen Sätze.

            Chat-Verlauf: {student_msgs}
            """
            feedback = get_completion([{"role": "user", "content": analysis_prompt}])
            st.markdown(f'<div style="background:white; border-top:4px solid #7c2d12; padding:30px; border-radius:8px; box-shadow:0 10px 30px rgba(0,0,0,0.1); margin-top:20px;"><h3 style="color:#7c2d12; font-family:Crimson Pro;">Review Report</h3><div style="font-size:1.1rem; line-height:1.6;">{feedback}</div></div>', unsafe_allow_html=True)
