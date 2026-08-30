import httpx
import streamlit as st
st.title("⚙️ MLOps & System Status")
if not st.session_state.get("token"):
    st.warning("Please sign in from the main page.")
    st.stop()
r = httpx.get(
    f"{st.session_state.api_url}/api/v1/agents/status",
    headers={"Authorization": f"Bearer {st.session_state.token}"},
    timeout=30,
)
if r.is_success:
    data = r.json()
    st.success(f"System: {data['status']}")
    st.dataframe(data["agents"], use_container_width=True)
else:
    st.error(r.text)
st.caption("MLflow is available on port 5000 in the Docker Compose environment.")
