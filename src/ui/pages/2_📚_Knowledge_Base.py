import httpx
import streamlit as st

st.title("📚 Knowledge Base")
if not st.session_state.get("token"):
    st.warning("Please sign in from the main page.")
    st.stop()

files = st.file_uploader("Upload PDF, DOCX, TXT or Markdown", type=["pdf","docx","txt","md"], accept_multiple_files=True)
if st.button("Upload selected files", disabled=not files):
    for file in files or []:
        r = httpx.post(
            f"{st.session_state.api_url}/api/v1/documents",
            headers={"Authorization": f"Bearer {st.session_state.token}"},
            files={"file": (file.name, file.getvalue(), file.type)},
            timeout=120,
        )
        st.success(f"Queued {file.name}") if r.is_success else st.error(r.text)

r = httpx.get(
    f"{st.session_state.api_url}/api/v1/documents",
    headers={"Authorization": f"Bearer {st.session_state.token}"},
    timeout=30,
)
if r.is_success:
    st.dataframe(r.json(), use_container_width=True)
