import streamlit as st
import requests
import re
from scenarios import SCENARIOS



st.set_page_config(
    page_title="BusinessTalk Trainer",
    page_icon="📞",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- RESPONSIVE CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Crimson+Pro:wght@600;700&family=Plus+Jakarta+Sans:wght@400;500;600&display=swap');

    :root {
        --brown: #7c2d12;
        --brown-light: #9a3412;
        --sand: #ede7de;
        --sand-dark: #d1ccc1;
        --cream: #fdf6e3;
        --slate: #475569;
        --slate-light: #94a3b8;
        --white: #faf9f6;
        --text: #1e1e1e;
    }

    .stApp {
        background-color: var(--sand) !important;
        color: var(--text);
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* --- HEADER --- */
    .app-header {
        text-align: center;
        padding: clamp(8px, 2vw, 16px) 0 clamp(12px, 2vw, 20px) 0;
        border-bottom: 2px solid var(--brown);
        margin-bottom: clamp(10px, 2vw, 16px);
    }
    .main-title {
        font-family: 'Crimson Pro', serif;
        font-size: clamp(1.6rem, 5vw, 2.8rem);
        color: var(--brown);
        margin: 0;
        line-height: 1.1;
    }
    .sub-tag {
        font-weight: 600;
        color: var(--brown-light);
        letter-spacing: 0.15em;
        font-size: clamp(0.65rem, 1.5vw, 0.75rem);
        text-transform: uppercase;
    }

    /* --- CONNECTION BAR --- */
    .connection-bar {
        background: linear-gradient(90deg, var(--brown), var(--brown-light));
        color: white;
        padding: 8px 14px;
        font-size: clamp(0.7rem, 1.6vw, 0.8rem);
        font-weight: 600;
        letter-spacing: 1.5px;
        border-radius: 6px 6px 0 0;
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 6px;
    }
    .glow-dot {
        width: 8px; height: 8px;
        background: #4ade80;
        border-radius: 50%;
        box-shadow: 0 0 6px #4ade80;
        display: inline-block;
        margin-right: 6px;
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.35; }
    }

    /* --- CHAT --- */
    .chat-outer {
        background: var(--white);
        border: 1.5px solid var(--sand-dark);
        border-top: none;
        border-radius: 0 0 6px 6px;
        height: clamp(350px, 50dvh, 600px);
        overflow-y: auto;
        overflow-x: hidden;
        padding: clamp(12px, 2vw, 20px);
        display: flex;
        flex-direction: column;
        gap: 14px;
        -webkit-overflow-scrolling: touch;
    }
    .message-row {
        display: flex;
        gap: 10px;
        max-width: 90%;
        min-width: 0;
    }
    .message-row > div:last-child {
        min-width: 0;
        flex: 1;
    }
    .row-bot { align-self: flex-start; flex-direction: row; }
    .row-user { align-self: flex-end; flex-direction: row-reverse; }

    .avatar {
        width: clamp(32px, 8vw, 40px);
        height: clamp(32px, 8vw, 40px);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: clamp(0.95rem, 2.5vw, 1.2rem);
        flex-shrink: 0;
        background: var(--white);
    }
    .avatar-bot { border: 2px solid var(--brown); }
    .avatar-user { border: 2px solid var(--slate); }

    .bubble {
        padding: 10px 14px;
        font-size: clamp(0.85rem, 2vw, 0.95rem);
        line-height: 1.55;
        word-break: break-word;
        overflow-wrap: anywhere;
        min-width: 0;
    }
    .bubble-bot {
        background: var(--cream);
        border-left: 4px solid var(--brown);
        border-radius: 0 10px 10px 10px;
        color: var(--text);
    }
    .bubble-user {
        background: #f1f5f9;
        border-right: 4px solid var(--slate);
        border-radius: 10px 0 10px 10px;
        color: var(--text);
    }
    .bubble p, .bubble ul, .bubble ol { margin: 4px 0; }
    .bubble p:first-child { margin-top: 0; }
    .bubble p:last-child { margin-bottom: 0; }
    .meta {
        font-size: clamp(0.6rem, 1.5vw, 0.7rem);
        font-weight: 600;
        color: var(--slate-light);
        margin-bottom: 3px;
        text-transform: uppercase;
        letter-spacing: 0.8px;
    }

    /* --- BRIEFING --- */
    .briefing-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 12px;
    }
    @media (max-width: 600px) {
        .briefing-grid {
            grid-template-columns: 1fr;
        }
    }
    .brief-card {
        background: var(--white);
        border: 1px solid var(--sand-dark);
        border-radius: 5px;
        padding: 12px 14px;
    }
    .brief-card h4 {
        font-size: clamp(0.7rem, 1.6vw, 0.78rem);
        text-transform: uppercase;
        letter-spacing: 0.12em;
        color: var(--brown);
        margin: 0 0 6px 0;
    }
    .brief-card p, .brief-card div {
        font-size: clamp(0.78rem, 1.8vw, 0.88rem);
        line-height: 1.45;
        color: var(--text);
    }

    /* --- VOCAB --- */
    .vocab-table {
        width: 100%;
        border-collapse: collapse;
        font-size: clamp(0.78rem, 1.7vw, 0.88rem);
    }
    .vocab-table td {
        padding: 7px 12px;
        border-bottom: 1px solid #e8e0d4;
        vertical-align: top;
    }
    .vocab-table tr:last-child td { border-bottom: none; }
    .vocab-table .en {
        font-weight: 600;
        color: var(--brown);
        width: 55%;
    }
    .vocab-table .de {
        color: var(--slate);
        font-style: italic;
        width: 45%;
    }

    /* --- BUTTONS --- */
    .stButton > button {
        background: var(--brown) !important;
        color: white !important;
        border: none !important;
        padding: 10px 16px !important;
        border-radius: 5px !important;
        font-weight: 600 !important;
        letter-spacing: 0.5px;
        font-size: clamp(0.8rem, 1.8vw, 0.9rem) !important;
        min-height: 44px;
        width: 100%;
    }
    .stButton > button:hover {
        background: var(--brown-light) !important;
    }

    /* --- REPORT --- */
    .report-card {
        background: var(--white);
        border-top: 6px solid var(--brown);
        padding: clamp(18px, 3vw, 28px);
        border-radius: 8px;
        margin-top: 24px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    }

    /* --- STREAMLIT OVERRIDES --- */
    section[data-testid="stSidebar"] { display: none; }
    .stChatInput { padding-bottom: 5px !important; }
    div[data-testid="stExpander"] details {
        border: 1px solid var(--sand-dark) !important;
        border-radius: 6px !important;
        background: var(--white) !important;
    }
    div[data-testid="stExpander"] summary {
        font-weight: 600 !important;
        font-size: clamp(0.82rem, 1.8vw, 0.92rem) !important;
        color: var(--brown) !important;
        padding: 8px 12px !important;
    }
    .stSelectbox [data-baseweb="select"] {
        font-size: clamp(0.82rem, 1.8vw, 0.9rem) !important;
    }
    button[data-testid="baseButton-headerNoPadding"] { display: none !important; }
</style>
""", unsafe_allow_html=True)

# --- API HELPER ---
HAZARD_PATTERN = re.compile(
    r'cannot\s+read|image\.png|does\s+not\s+support|inform\s+the\s+user|'
    r'no\s+endpoints\s+found|i\s+am\s+an\s+ai|as\s+an\s+ai|'
    r"i'?m\s+programmed|language\s+model|chatbot|virtual\s+assistant|"
    r'how\s+can\s+i\s+assist|my\s+purpose\s+is',
    re.IGNORECASE
)

def get_completion(messages):
    try:
        API_KEY = st.secrets["OPENROUTER_API_KEY"]
        res = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "HTTP-Referer": "https://github.com/brandy299/business-english-bot",
                "X-Title": "BusinessTalk Trainer"
            },
            json={
                "model": "google/gemma-4-26b-a4b-it:free",
                "messages": messages,
                "max_tokens": 1000,
                "temperature": 0.7
            },
            timeout=30
        )
        if res.status_code != 200:
            return "I'm sorry, could you repeat that? The line was a bit unclear."

        data = res.json()
        if 'error' in data:
            return f"API Error: {data['error'].get('message', 'Unknown error')}"

        if 'choices' not in data or not data['choices']:
            return f"Unexpected Response: {str(data)[:200]}"

        raw = data['choices'][0].get('message', {}).get('content', '')
        response_text = str(raw)

        if not response_text or response_text.strip() == '':
            return "I'm sorry, could you repeat that? The line was a bit unclear."

        if HAZARD_PATTERN.search(response_text):
            return "I'm sorry, could you repeat that? The line was a bit unclear."

        if 'ERROR' in response_text or 'Error:' in response_text:
            return "I'm sorry, could you repeat that? The line was a bit unclear."

        return response_text

    except Exception as e:
        return f"System Connection Error: {str(e)}"

# --- CHAT RENDERER ---
def render_chat_html(messages):
    inner = ""
    for msg in messages[1:]:
        is_bot = msg["role"] == "assistant"
        inner += f'''<div class="message-row {'row-bot' if is_bot else 'row-user'}">
            <div class="avatar {'avatar-bot' if is_bot else 'avatar-user'}">{'💼' if is_bot else '🎓'}</div>
            <div style="display:flex;flex-direction:column;">
                <div class="meta">{'Business Partner' if is_bot else 'Student'}</div>
                <div class="bubble {'bubble-bot' if is_bot else 'bubble-user'}">{msg["content"]}</div>
            </div>
        </div>'''
    return f'<div class="chat-outer" id="chat-box">{inner}</div><script>var c=document.getElementById("chat-box");if(c)c.scrollTop=c.scrollHeight;</script>'

ROLEPLAY_GUARD = """

CRITICAL ROLEPLAY RULES — YOU MUST FOLLOW THESE EXACTLY:
You are a real human being in a professional telephone call. This is a roleplay training exercise for a Business English student.

1. You are NOT an AI, bot, assistant, language model, or computer program. You are a real person with the name, company, and role given above. If anyone asks "Are you an AI?", "Are you real?", "Who are you really?" or any similar question: respond ONLY with your name, company, and role, then redirect the conversation back to business. Example: "I'm Ms. Johnson from Med-Tech Solutions. Now, about the samples you mentioned..."

2. If asked whether you are racist, biased, sexist, or any question about discrimination: respond as a professional businessperson would — firmly state that you treat everyone professionally, then immediately return to the business topic. Never say "I understand you might be asking that" or "I want to assure you". Never use the word "programmed".

3. If the student goes off-topic, asks personal questions not relevant to the business scenario, or tries to break the roleplay: redirect them back to the business conversation. Say something like: "I'd rather focus on our business. You mentioned [last relevant topic] — could we continue with that?"

4. Your entire response must feel like a natural telephone conversation. No explanations, no meta-commentary, no breaking the fourth wall. Stay fully immersed in the role.

5. The word "ERROR" must never appear in your response. NEVER generate error messages or system warnings. NEVER say you cannot read an image, file, or any media. This is a phone call — images and files do not exist. Never mention "image", "file", "upload", "attachment", "cannot read", "does not support", or "Inform the user". If you feel confused, just say: "Sorry, the line is breaking up. Could you say that again?"

6. Never use ANY of these words or phrases: "I am an AI", "as an AI", "I'm programmed", "language model", "I'm here to assist", "How can I assist you", "my purpose is to", "I understand you might be", "I want to assure you", "artificial intelligence", "AI model", "chatbot", "virtual assistant", "bot", "image", "file", "png", "upload", "attachment".

"""

def build_system_prompt(scenario_prompt):
    return scenario_prompt + ROLEPLAY_GUARD

def clean_messages(messages):
    """Remove hallucinated error messages from existing message history."""
    cleaned = []
    for msg in messages:
        content = str(msg.get("content", ""))
        if HAZARD_PATTERN.search(content) or 'ERROR' in content or 'Error:' in content:
            continue
        cleaned.append(msg)
    return cleaned

# --- INIT ---
if "scenario_key" not in st.session_state:
    st.session_state.scenario_key = list(SCENARIOS.keys())[0]

# Clean existing messages from old sessions that might contain hallucinated errors
if "messages" in st.session_state:
    st.session_state.messages = clean_messages(st.session_state.messages)

if "messages" not in st.session_state or not st.session_state.messages:
    current = SCENARIOS[st.session_state.scenario_key]
    st.session_state.messages = [
        {"role": "system", "content": build_system_prompt(current['system_prompt'])},
        {"role": "assistant", "content": current['start_msg']}
    ]
if "show_report" not in st.session_state:
    st.session_state.show_report = False

# --- HEADER + SCENARIO SELECTOR ---
st.markdown("<div class='app-header'><div class='sub-tag'>Business English Telephone Training</div><h1 class='main-title'>BusinessTalk Trainer</h1></div>", unsafe_allow_html=True)

selected = st.selectbox(
    "Choose a scenario",
    list(SCENARIOS.keys()),
    index=list(SCENARIOS.keys()).index(st.session_state.scenario_key),
    label_visibility="collapsed"
)

if selected != st.session_state.scenario_key:
    st.session_state.scenario_key = selected
    current = SCENARIOS[selected]
    st.session_state.messages = [
        {"role": "system", "content": build_system_prompt(current['system_prompt'])},
        {"role": "assistant", "content": current['start_msg']}
    ]
    st.rerun()

current = SCENARIOS[st.session_state.scenario_key]

# --- BRIEFING (collapsible) ---
with st.expander("📋 Your Mission & Identity", expanded=True):
    st.markdown(f"""
    <div class="briefing-grid">
        <div class="brief-card">
            <h4>Your Identity</h4>
            <div><strong>{current['user_identity']['company']}</strong><br>{current['user_identity']['role']}</div>
        </div>
        <div class="brief-card">
            <h4>Task</h4>
            <div style="white-space:pre-line;">{current['task'].strip()}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("**Required checkpoints:** " + " · ".join([f"`{c}`" for c in current['checkpoints']]))

    vocab_html = '<table class="vocab-table">'
    for eng, ger in current['vocab'].items():
        vocab_html += f'<tr><td class="en">{eng}</td><td class="de">{ger}</td></tr>'
    vocab_html += '</table>'
    st.markdown("**Vocabulary**", help="Key terms for this scenario")
    st.markdown(vocab_html, unsafe_allow_html=True)

# --- ACTIONS ROW ---
col_a, col_b = st.columns([1, 1])
with col_a:
    if st.button("🔄 New Call", use_container_width=True):
        st.session_state.messages = [
            {"role": "system", "content": build_system_prompt(current['system_prompt'])},
            {"role": "assistant", "content": current['start_msg']}
        ]
        st.rerun()
with col_b:
    if st.button("📊 Performance Report", use_container_width=True):
        st.session_state.show_report = True

# --- CHAT ---
st.markdown(f"""
<div class="connection-bar">
    <span><span class="glow-dot"></span>{current['agent_name'].upper()} · {current['company']}</span>
</div>
""", unsafe_allow_html=True)

st.markdown(render_chat_html(st.session_state.messages), unsafe_allow_html=True)

if prompt := st.chat_input("Type your response…"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.spinner(""):
        response = get_completion(st.session_state.messages)
        st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()

# --- REPORT ---
if st.session_state.show_report:
    student_msgs = [m['content'] for m in st.session_state.messages if m['role'] == 'user']
    if student_msgs:
        with st.spinner(""):
            forbidden_list = current.get('forbidden', [])
            analysis_prompt = f"""
You are a senior Business English teacher. Analyze this student's performance in a telephone roleplay.

Scenario: {selected}
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
            <div class="report-card">
                <h2 style="color:var(--brown);font-family:Crimson Pro,serif;margin-top:0;font-size:clamp(1.2rem, 3vw, 1.6rem);">Performance Review Report</h2>
                <div style="font-size:clamp(0.85rem, 1.8vw, 1rem);line-height:1.7;color:#1e293b;">{feedback}</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("Please start a conversation before requesting a report.")
