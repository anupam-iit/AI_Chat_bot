import streamlit as st
from google import genai
from google.genai import types

# 1. PAGE CONFIG & MODERN UI STYLING
st.set_page_config(page_title="Personalised AI Chatbot", page_icon="🤖", layout="wide")

# Custom CSS for Header, Footer, and High-Contrast Chat

# --- HEADER & FOOTER MODIFICATION CODE ---
st.markdown("""
    <style>
    /* 1. THE HEADER */
    .custom-header {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 60px;
        background: rgba(30, 41, 59, 0.8); /* Semi-transparent Dark Slate */
        backdrop-filter: blur(10px);      /* Glass effect */
        color: white;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 20px;
        font-weight: bold;
        letter-spacing: 1px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        z-index: 999999; /* Higher than any Streamlit element */
    }

    /* 2. THE FOOTER */
    .custom-footer {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        height: 50px;
        background: #020617;
        color: #64748b;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 12px;
        z-index: 999999;
    }

    /* 3. PUSH DOWN THE CONTENT (Crucial) */
    /* This ensures the chat doesn't hide under the header */
    .main .block-container {
        padding-top: 80px !important; 
        padding-bottom: 50px !important;
    }
    
    /* Hide Streamlit's default header/menu for a cleaner look */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    
    <div class="custom-header">
        🎓 Anupam's Personalized AI Chatbot
    </div>
    
    <div class="custom-footer">
        Developed by Anupam Roy • anu.rex@gmail.com • © PMIT, JU
    </div>
    """, unsafe_allow_html=True)

# 2. INITIALIZE API & SESSION STATE
api_key = st.secrets["GOOGLE_API_KEY"]


if "messages" not in st.session_state:
    st.session_state.messages = []
if "history_list" not in st.session_state:
    st.session_state.history_list = []

# 3. SIDEBAR: SEARCH LIST (CONVERSATION HISTORY)
with st.sidebar:
    st.title("📚 Search History")
    if not st.session_state.history_list:
        st.write("No previous searches yet.")
    else:
        for i, item in enumerate(reversed(st.session_state.history_list)):
            st.button(f"🔍 {item[:25]}...", key=f"hist_{i}", use_container_width=True)
    
    st.divider()
    if st.button("🗑️ Clear All History", use_container_width=True):
        st.session_state.messages = []
        st.session_state.history_list = []
        st.rerun()

# 4. MAIN CHAT AREA
# Icons: 'user' uses default, 'assistant' uses custom AI icon
for message in st.session_state.messages:
    avatar = "🤖" if message["role"] == "assistant" else "👤"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("Ask Anything..."):
    # Save search title to sidebar list
    if prompt not in st.session_state.history_list:
        st.session_state.history_list.append(prompt)
    
    # Display user message
    st.chat_message("user", avatar="👤").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Direct Response Rendering (No hidden status box)
    with st.chat_message("assistant", avatar="🤖"):
        response_placeholder = st.empty()
        full_response = ""
        
        try:
            responses = client.models.generate_content_stream(
                model="gemini-2.5-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction="You are a professional Academic Agent. Be direct, formal, and precise.",
                    temperature=0.7
                )
            )
            
            for chunk in responses:
                full_response += chunk.text
                # Streaming directly to the UI
                response_placeholder.markdown(full_response + "▌")
            
            response_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"Error: {e}")
