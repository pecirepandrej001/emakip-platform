from pathlib import Path
import httpx
import streamlit as st
from src.ui.components.sidebar import render_sidebar
from src.ui.components.chat_interface import render_chat

st.set_page_config(page_title="EMAKIP", page_icon="🧠", layout="wide")
css = Path(__file__).with_name("assets").joinpath("style.css").read_text(encoding="utf-8")
st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
render_sidebar()

st.title("Enterprise Multi-Agent Knowledge & Intelligence Platform")
st.caption("LangGraph orchestration · Hybrid RAG · SQL analytics · MLOps")

if "token" not in st.session_state:
    tab_login, tab_register = st.tabs(["Login", "Register"])
    with tab_login:
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")
        if st.button("Login", use_container_width=True):
            r = httpx.post(f"{st.session_state.api_url}/api/v1/auth/login",
                           json={"email": email, "password": password}, timeout=30)
            if r.is_success:
                st.session_state.token = r.json()["access_token"]
                st.rerun()
            else:
                st.error("Login failed")
    with tab_register:
        full_name = st.text_input("Full name")
        email2 = st.text_input("Email", key="register_email")
        password2 = st.text_input("Password", type="password", key="register_password")
        if st.button("Create account", use_container_width=True):
            r = httpx.post(f"{st.session_state.api_url}/api/v1/auth/register",
                           json={"email": email2, "full_name": full_name, "password": password2}, timeout=30)
            if r.is_success:
                st.session_state.token = r.json()["access_token"]
                st.rerun()
            else:
                st.error(r.text)
    st.stop()

render_chat()
