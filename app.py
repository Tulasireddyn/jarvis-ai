
import streamlit as st
import time
from dotenv import load_dotenv
load_dotenv()
from utils.llm_handler import JarvisLLM
from utils.vector_db import JarvisMemory

# Page Config
st.set_page_config(page_title="Jarvis AI", page_icon="🤖", layout="wide")

# Custom CSS for "Premium" look
st.markdown("""
<style>
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
    }
    .stTextInput > div > div > input {
        background-color: #262730;
        color: #ffffff;
    }
    .stChatInput > div > div > textarea {
        background-color: #262730;
        color: #ffffff;
    }
    h1 {
        background: -webkit-linear-gradient(45deg, #FF6B6B, #4ECDC4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Backend
if "memory" not in st.session_state:
    st.session_state.memory = JarvisMemory()
if "llm" not in st.session_state:
    st.session_state.llm = JarvisLLM()

# Sidebar - Knowledge Base
with st.sidebar:
    st.title("🧠 Knowledge Base")
    st.markdown("Add documents to Jarvis's memory.")
    
    new_doc = st.text_area("Add Context/Knowledge:", height=150)
    if st.button("Add to Memory"):
        if new_doc:
            st.session_state.memory.save_context(new_doc)
            st.success("Added to memory!")
        else:
            st.warning("Please enter some text.")

# Main Chat Interface
st.title("🤖 Jarvis Assistant")
st.caption("Powered by Local LLM & Vector Database")

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("Ask Jarvis something..."):
    # Display User Message
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Retrieve Context
    context = st.session_state.memory.retrieve_context(prompt)
    
    # Generate Response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = st.session_state.llm.generate_response(prompt, context)
        
        # Simulate typing effect
        displayed_response = ""
        for chunk in full_response.split():
            displayed_response += chunk + " "
            time.sleep(0.05)
            message_placeholder.markdown(displayed_response + "▌")
        message_placeholder.markdown(displayed_response)
        
    st.session_state.messages.append({"role": "assistant", "content": displayed_response})
