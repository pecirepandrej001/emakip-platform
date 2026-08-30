import streamlit as st
from src.ui.components.chat_interface import render_chat
st.title("💬 Enterprise Chat")
if not st.session_state.get("token"):
    st.warning("Please sign in from the main page.")
else:
    render_chat()
