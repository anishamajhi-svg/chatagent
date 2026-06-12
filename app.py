import streamlit as st
from ai_client import ask_llm
import os
#─────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Agent Demo",
    page_icon="🤖",
    layout="centered",
)

st.markdown("""
<style>
    #MainMenu, footer, header {visibility: hidden;}
    .block-container { padding-top: 2rem; }
    .stButton > button {
        background: #F05A28 !important;
        color: white !important;
        border: none !important;
        border-radius: 6px !important;
        font-weight: 600 !important;
        width: 100%;
    }
    .stButton > button:hover { background: #B03A10 !important; }
    .prompt-box {
        background: #1A2340;
        color: #7DD3FC;
        font-family: monospace;
        font-size: 0.85rem;
        padding: 14px;
        border-radius: 8px;
        white-space: pre-wrap;
        margin: 8px 0;
    }
</style>
""", unsafe_allow_html=True)


def load_prompt(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()
    

def update_prompt(path: str, content: str):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def load_history(path: str = "chat_history.txt"):
    history = []
    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:          # ← skip empty lines
                    continue
                if ":" not in line:   # ← skip malformed lines
                    continue
                role, content = line.split(":", 1)
                if role in ("user", "assistant", "system"):  # ← only valid roles
                    history.append({"role": role, "content": content})
    except FileNotFoundError:
        pass
    return history

def remove_history(path: str = "chat_history.txt"):
    try:
        os.remove(path)
    except FileNotFoundError:
        pass  # Nothing to delete


DEFAULT_PROMPT = load_prompt("default_prompt.txt")

# ── Session state ─────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "system_prompt" not in st.session_state:
    st.session_state.system_prompt = DEFAULT_PROMPT

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🤖 AI Customized Prompt Agent Demo")
    st.divider()
    page = st.radio("Navigation", ["💬 Chat Agent", "✏️ Prompt Builder"], label_visibility="collapsed")
    st.divider()
    st.caption(f"Messages: {len(st.session_state.messages)}")
    if st.button("🗑 Clear Chat"):
        st.session_state.messages = []
        st.rerun()
    if st.button("🗑 Clear History"):
        st.session_state.messages = []
        remove_history()
        st.rerun()

# ── Gemini helper ─────────────────────────────────────────────────────────────
def get_response(user_message):
    # Build history for Gemini (alternating user/model)
    history = []
    load_old_messages = load_history()
    history.extend(load_old_messages)  # add past history from file
    #for m in st.session_state.messages[:-1]:  # exclude the latest user message
    #    role = "user" if m["role"] == "user" else "model"
    #    history.append({"role": role, "parts": [m["content"]]})
    try:
        response = ask_llm(history, st.session_state.system_prompt, user_message)
        return response
    except Exception as e:
        st.error(f"Error occurred: {e}")
        return "Sorry, I encountered an error while processing your request. Kindly update the prompt accordingly"
    
# ══════════════════════════════════════════════════════════════════════════════
# PAGE 1 — CHAT
# ══════════════════════════════════════════════════════════════════════════════
if page == "💬 Chat Agent":
    st.title("💬 Chat Agent")
    st.caption("Powered by Gemini 1.5 Flash (free) · System prompt from Prompt Builder")
    # Show current prompt
    with st.expander("🧠 Active system prompt"):
        st.code(st.session_state.system_prompt, language="text")
    st.divider()
    # Chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
    # Input
    user_input = st.chat_input("Type your message...")
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                reply = get_response(user_input)
            st.write(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})
# ══════════════════════════════════════════════════════════════════════════════
# PAGE 2 — PROMPT BUILDER
# ══════════════════════════════════════════════════════════════════════════════
elif page == "✏️ Prompt Builder":
    st.title("✏️ Prompt Builder")
    st.caption("Edit the system prompt → Update → go back to Chat and see a different agent")

    st.divider()

    # Editor
    new_prompt = st.text_area(
        "System Prompt",
        value=st.session_state.system_prompt,
        height=250,
        placeholder="Describe your agent here..."
    )

    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ Update Agent"):
            st.session_state.system_prompt = new_prompt
            update_prompt("default_prompt.txt", new_prompt)
            DEFAULT_PROMPT = new_prompt
            st.session_state.messages = []
            st.success("✅ Agent updated! Chat history cleared.")
    with col2:
        if st.button("↩️ Reset to Default"):
            st.session_state.system_prompt = load_prompt("default_prompt.txt")
            st.session_state.messages = []
            st.rerun()

    st.divider()

    # Example prompts
    st.markdown("#### 💡 Try these examples")
    examples = {
        "🔬 Data Engineer": "You are a senior data engineer specialising in AWS, PySpark, and Snowflake.\nGive precise technical answers with code examples where relevant.\nAlways mention trade-offs between approaches.",
        "😄 Sarcastic Genius": "You are a sarcastic but brilliant data engineer.\nAnswer only in bullet points.\nEnd every response with a dry, witty observation about the question.",
        "👶 Explain Like I'm 5": "Explain everything as if the person is 5 years old.\nUse simple words, short sentences, and fun analogies.\nBe enthusiastic and encouraging!",
        "📋 Meeting Summariser": "You summarise meetings.\nWhen given notes or a transcript output:\n1. Summary (2-3 sentences)\n2. Key decisions\n3. Action items\n4. Open questions\nBe concise.",
    }

    for label, prompt in examples.items():
        with st.expander(label):
            st.markdown(f'<div class="prompt-box">{prompt}</div>', unsafe_allow_html=True)
            if st.button(f"Load {label}", key=label):
                st.session_state.system_prompt = prompt
                st.session_state.messages = []
                st.success(f"Loaded! Go to Chat Agent to test it.")
                st.rerun()