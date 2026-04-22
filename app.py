import streamlit as st
import requests
from scenarios import SCENARIOS

# --- CONFIGURATION ---
st.set_page_config(
    page_title="Business English | Workbench", 
    page_icon="🎓", 
    layout="wide"
)

# --- ARCHITECTURAL CSS (THE FIX) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Crimson+Pro:wght@700&family=Plus+Jakarta+Sans:wght@400;600&display=swap');

    /* 1. Global Background Fix - Gekoppelt an .stApp */
    .stApp {
        background-color: #e5dfd3 !important; /* Dunklerer Sandstein */
        color: #2d2d2d;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* 2. Header Area */
    .app-header {
        text-align: left;
        padding: 20px 0 40px 0;
    }
    .main-title {
        font-family: 'Crimson Pro', serif;
        font-size: 3.5rem;
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

    /* 3. The Assignment Side (Paper style) */
    .assignment-container {
        background: #ffffff;
        padding: 30px;
        border-radius: 4px;
        border: 1px solid #d1ccc1;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        margin-bottom: 25px;
    }

    /* 4. Vocabulary Masters */
    .v-tag {
        display: inline-block;
        background: #fef2f2;
        color: #9a3412;
        padding: 5px 12px;
        border-radius: 4px;
        margin: 4px;
        font-size: 0.85rem;
        font-weight: bold;
        border: 1px solid #fee2e2;
    }

    /* 5. Custom Button Styling */
    .stButton>button {
        background-color: #7c2d12 !important;
        color: #ffffff !important;
        border: none !important;
        padding: 12px 24px !important;
        border-radius: 4px !important;
        font-weight: bold !important;
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# --- API HELPER ---
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
        return f"Error: {str(e)}"

# --- CHAT RENDERER (THE CORE FIX) ---
def render_chat_html(messages):
    chat_html = """
    <style>
        .chat-master-container {
            background-color: #ffffff !important; /* PURE WHITE */
            border: 2px solid #d1ccc1;
            border-radius: 12px;
            box-shadow: 0 20px 50px rgba(0,0,0,0.15);
            height: 550px;
            overflow-y: scroll;
            padding: 25px;
            display: flex;
            flex-direction: column;
            gap: 20px;
            font-family: 'Plus Jakarta Sans', sans-serif;
        }
        .chat-master-container::-webkit-scrollbar {
            width: 8px;
        }
        .chat-master-container::-webkit-scrollbar-thumb {
            background: #d1ccc1;
            border-radius: 10px;
        }
        .bubble {
            max-width: 80%;
            padding: 15px 20px;
            font-size: 1.05rem;
            line-height: 1.5;
            position: relative;
        }
        .bubble-bot {
            align-self: flex-start;
            background-color: #fdf6e3;
            border-left: 5px solid #7c2d12;
            border-radius: 0 10px 10px 10px;
            color: #1a1a1a;
        }
        .bubble-user {
            align-self: flex-end;
            background-color: #f1f5f9;
            border-right: 5px solid #475569;
            border-radius: 10px 0 10px 10px;
            color: #1a1a1a;
            text-align: right;
        }
        .bubble-meta {
            font-size: 0.7rem;
            font-weight: bold;
            text-transform: uppercase;
            color: #94a3b8;
            margin-bottom: 5px;
        }
    </style>
    <div class="chat-master-container" id="chat-box">
    """
    
    for msg in messages[1:]:
        is_bot = msg["role"] == "assistant"
        align = "flex-start" if is_bot else "flex-end"
        cls = "bubble-bot" if is_bot else "bubble-user"
        lbl = "BUSINESS PARTNER" if is_bot else "YOU (STUDENT)"
        
        chat_html += f"""
        <div style="display: flex; flex-direction: column; align-items: {align};">
            <div class="bubble-meta">{lbl}</div>
            <div class="bubble {cls}">{msg['content']}</div>
        </div>
        """
    
    chat_html += """
    </div>
    <script>
        var chatBox = document.getElementById('chat-box');
        chatBox.scrollTop = chatBox.scrollHeight;
    </script>
    """
    return chat_html

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("<h2 style='color: #7c2d12;'>TeacherHub</h2>", unsafe_allow_html=True)
    st.markdown("---")
    selected_scenario_name = st.selectbox("Current Unit", list(SCENARIOS.keys()))
    current = SCENARIOS[selected_scenario_name]
    
    if st.button("RESTART MISSION", use_container_width=True):
        st.session_state.messages = [
            {"role": "system", "content": current['system_prompt']},
            {"role": "assistant", "content": current['start_msg']}
        ]
        st.rerun()

# --- MAIN PAGE ---
st.markdown("""
    <div class='app-header'>
        <div class='sub-tag'>Kaufmännisches Berufskolleg NRW</div>
        <h1 class='main-title'>English Telephoning Coach</h1>
    </div>
""", unsafe_allow_html=True)

layout_left, layout_right = st.columns([1, 1.4], gap="large")

with layout_left:
    st.markdown(f"""
    <div class="assignment-container">
        <div class='sub-tag' style='margin-bottom:10px;'>Your Assignment</div>
        <div style="font-family: Georgia, serif; font-size: 1.25rem; line-height: 1.6;">{current["task"]}</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### Mastery Vocabulary")
    v_html = "".join([f'<span class="v-tag">{w}</span>' for w in current['vocab']])
    st.markdown(v_html, unsafe_allow_html=True)

with layout_right:
    # State Init
    if "messages" not in st.session_state or st.session_state.get('last_scenario') != selected_scenario_name:
        st.session_state.messages = [
            {"role": "system", "content": current['system_prompt']},
            {"role": "assistant", "content": current['start_msg']}
        ]
        st.session_state.last_scenario = selected_scenario_name

    # RENDER THE HARD-CONTRAST CHAT BLOCK
    st.markdown(render_chat_html(st.session_state.messages), unsafe_allow_html=True)

    # USER INPUT
    if prompt := st.chat_input("Enter your response..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Wir müssen neu laden, damit die UI den Bot-Spinner zeigt
        with st.spinner("Analyzing protocol..."):
            response = get_completion(st.session_state.messages)
            st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()

# --- EVALUATION ---
st.markdown("<br>", unsafe_allow_html=True)
if st.button("📊 GENERATE FINAL EVALUATION", use_container_width=True):
    student_msgs = [m['content'] for m in st.session_state.messages if m['role'] == 'user']
    if student_msgs:
        with st.spinner("Reviewing dialogue protocols..."):
            feedback = get_completion([{"role": "user", "content": f"Analysiere diesen Chat auf Deutsch (Feedback zu Höflichkeit, Vokabeln {current['vocab']}, 3 Korrektur-Sätze): {student_msgs}"}])
            st.markdown(f"""
                <div style="background: #ffffff; border-top: 5px solid #7c2d12; padding: 40px; border-radius: 8px; box-shadow: 0 10px 40px rgba(0,0,0,0.1); margin-top: 30px;">
                    <h3 style="color: #7c2d12; font-family: Crimson Pro; font-size: 2.2rem;">Academic Review Report</h3>
                    <div style="font-size: 1.2rem; line-height: 1.7; color: #374151;">{feedback}</div>
                </div>
            """, unsafe_allow_html=True)
