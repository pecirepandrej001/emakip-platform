import streamlit as st
from src.ui.components.metrics_dashboard import render_metrics
st.title("📊 Analytics & Reports")
if not st.session_state.get("token"):
    st.warning("Please sign in from the main page.")
else:
    render_metrics()
