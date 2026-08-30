import streamlit as st

def render_sidebar() -> None:
    with st.sidebar:
        st.markdown("### EMAKIP")
        st.caption("Enterprise Multi-Agent Intelligence")
        st.divider()
        st.session_state.setdefault("api_url", "http://api:8000")
        st.text_input("API URL", key="api_url")
        if st.session_state.get("token"):
            if st.button("Sign out", use_container_width=True):
                st.session_state.pop("token", None)
                st.rerun()
