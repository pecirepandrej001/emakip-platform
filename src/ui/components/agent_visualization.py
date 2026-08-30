import streamlit as st

def render_agent_steps(steps: list[dict]) -> None:
    st.markdown("#### Agent execution")
    for step in steps:
        st.markdown(
            f"<div class='agent-step'><b>{step.get('agent','agent')}</b> · "
            f"{step.get('status','')}</div>",
            unsafe_allow_html=True,
        )
    st.caption("These are execution-status events, not hidden chain-of-thought.")
