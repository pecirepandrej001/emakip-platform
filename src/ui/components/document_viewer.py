import streamlit as st

def render_document_viewer(name: str, content: bytes | None = None) -> None:
    st.markdown(f"**{name}**")
    if content:
        st.download_button("Download local preview copy", content, file_name=name)
