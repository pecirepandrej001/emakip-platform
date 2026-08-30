import httpx
import streamlit as st
from src.ui.components.agent_visualization import render_agent_steps

def render_chat() -> None:
    st.subheader("Enterprise Chat")
    history = st.session_state.setdefault("chat_history", [])
    for item in history:
        with st.chat_message(item["role"]):
            st.markdown(item["content"])

    prompt = st.chat_input("Ask about your knowledge base...")
    if not prompt:
        return

    history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Running agent workflow..."):
            response = httpx.post(
                f"{st.session_state.api_url}/api/v1/chat",
                headers={"Authorization": f"Bearer {st.session_state.token}"},
                json={"message": prompt},
                timeout=120,
            )
        if response.is_success:
            data = response.json()
            st.markdown(data["answer"])
            render_agent_steps(data.get("steps", []))
            if data.get("sources"):
                with st.expander("Sources"):
                    for source in data["sources"]:
                        st.markdown(f"**{source['filename']}**")
                        st.caption(source["text"][:700])
            history.append({"role": "assistant", "content": data["answer"]})
        else:
            st.error(response.text)
