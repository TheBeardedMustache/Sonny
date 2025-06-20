"""
home.py: Streamlit Home Page component for Sonny's Mercury Frontend.
"""
import streamlit as st
from backend.core.core_agent import symbolic_state

def home_page():
    """Render the home page UI."""
    st.title("Sonny - Lunar Venusian Martial Regulus")
    st.subheader("Welcome to Sonny's Mercury Frontend")
    st.subheader("Symbolic State")
    st.json(symbolic_state.get_state())
    st.markdown(
        """
Use the sidebar to select an automation path:
- Mercury: Frontend interface
- Silver: Desktop Automation
- Gold: Autonomous Coding
- Cinnabar: Natural Language Understanding
- Combined: Full Automation Workflow
"""
    )