import httpx
import streamlit as st

def render_metrics() -> None:
    response = httpx.get(
        f"{st.session_state.api_url}/api/v1/analytics",
        headers={"Authorization": f"Bearer {st.session_state.token}"},
        timeout=30,
    )
    if not response.is_success:
        st.error(response.text)
        return
    data = response.json()
    cols = st.columns(3)
    cols[0].metric("Users", data["users"])
    cols[1].metric("Documents", data["documents"])
    cols[2].metric("Conversations", data["conversations"])
