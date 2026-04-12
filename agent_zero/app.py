import streamlit as st
from agent import run_agent
from memory import get_all_memories, clear_memories

st.set_page_config(
    page_title="Agent Zero",
    page_icon="🤖",
    layout="wide"
)

st.markdown("""
<style>
    .stApp { background-color: #0e1117; }
    
    header[data-testid="stHeader"] {
        background-color: #0e1117;
    }
    
    * { color: #e6edf3 !important; }
    
    [data-testid="stChatMessage"] {
        background-color: #161b22 !important;
        border: 1px solid #30363d;
        border-radius: 8px;
        margin-bottom: 8px;
    }
    
    /* Tool call styling - slightly different color */
    .tool-box {
        background-color: #1c2a3a;
        border: 1px solid #1f6feb;
        border-radius: 6px;
        padding: 10px;
        margin: 5px 0;
        font-size: 13px;
    }
    
    [data-testid="stChatInputContainer"] {
        background-color: #161b22 !important;
        border: 1px solid #30363d !important;
        border-radius: 8px !important;
    }

    [data-testid="stChatInputContainer"]:focus-within {
        border: 1px solid #58a6ff !important;
    }

    .stChatInput, 
    .stChatInput *,
    [data-testid="stChatInput"],
    [data-testid="stChatInput"] * {
        background-color: #161b22 !important;
        background: #161b22 !important;
        border-color: #30363d !important;
        box-shadow: none !important;
    }

    [data-testid="stBottom"],
    [data-testid="stBottom"] > div {
        background-color: #0e1117 !important;
    }

    footer { display: none !important; }
            
    /* Fix sidebar background and text */
    [data-testid="stSidebar"] {
        background-color: #161b22 !important;
        border-right: 1px solid #30363d !important;
    }
    
    [data-testid="stSidebar"] * {
        color: #e6edf3 !important;
    }
    
    /* Fix sidebar buttons */
    [data-testid="stSidebar"] button {
        background-color: #21262d !important;
        border: 1px solid #30363d !important;
    }
    
    /* Fix placeholder text color */
    textarea::placeholder {
        color: #8b949e !important;
        opacity: 1 !important;
    }
    
    input::placeholder {
        color: #8b949e !important;
        opacity: 1 !important;
    }
</style>
""", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar
with st.sidebar:
    st.title("🤖 Agent Zero")
    st.divider()
    
    st.subheader("🧠 Long Term Memory")
    memories = get_all_memories()
    st.text(memories)
    
    st.divider()
    
    if st.button("🗑️ Clear Memories", use_container_width=True):
        clear_memories()
        st.success("Memories cleared!")
        st.rerun()
    
    if st.button("💬 Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

st.title("🤖 Agent Zero")
st.markdown("An AI agent that thinks, uses tools, and reasons to answer your questions.")
st.divider()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
        # Show thinking steps for assistant messages
        if message["role"] == "assistant" and "steps" in message:
            if message["steps"]:
                with st.expander("🧠 View agent thinking"):
                    for step in message["steps"]:
                        if step["type"] == "tool_call":
                            st.markdown(f"""
<div class="tool-box">
🔧 <b>Tool Called:</b> {step['tool']}<br>
📥 <b>Input:</b> {step['input']}
</div>
""", unsafe_allow_html=True)
                        elif step["type"] == "tool_result":
                            st.markdown(f"""
<div class="tool-box">
📤 <b>Result from</b> {step['tool']}:<br>
{step['output']}...
</div>
""", unsafe_allow_html=True)
                            
if prompt := st.chat_input("Ask me anything..."):
    # Display user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Run agent and display response
    with st.chat_message("assistant"):
        with st.spinner("Agent thinking..."):
            # Build chat history from session state
            chat_history = []
            for msg in st.session_state.messages:
                if msg["role"] == "user":
                    chat_history.append({"role": "user", "content": msg["content"]})
                elif msg["role"] == "assistant":
                    chat_history.append({"role": "assistant", "content": msg["content"]})
            
            result = run_agent(prompt, chat_history)
        
        answer = result["answer"]
        steps = result["steps"]
        
        st.markdown(answer)
        
        # Show thinking steps
        if steps:
            with st.expander("🧠 View agent thinking"):
                for step in steps:
                    if step["type"] == "tool_call":
                        st.markdown(f"""
<div class="tool-box">
🔧 <b>Tool Called:</b> {step['tool']}<br>
📥 <b>Input:</b> {step['input']}
</div>
""", unsafe_allow_html=True)
                    elif step["type"] == "tool_result":
                        st.markdown(f"""
<div class="tool-box">
📤 <b>Result from</b> {step['tool']}:<br>
{step['output']}...
</div>
""", unsafe_allow_html=True)
    
    # Save to history
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer,
        "steps": steps
    })

