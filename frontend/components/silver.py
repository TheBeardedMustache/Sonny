"""
silver.py: Streamlit UI for Silver Path (Desktop Automation).
"""
import streamlit as st
from backend.core.core_agent import symbolic_state

def silver_ui():
    """Render the Silver Path UI for desktop automation."""
    st.header("Silver Path: Desktop Automation")
    # Instantiate automation agent (allow patch via frontend.app)
    try:
        from frontend.app import SilverAutomation
    except ImportError:
        from backend.core.core_agent import SilverAutomation
    sa = SilverAutomation()
    x = st.number_input("X-coordinate", value=0)
    y = st.number_input("Y-coordinate", value=0)
    duration = st.number_input("Duration (seconds)", value=0.0)
    if st.button("Move Mouse"):
        try:
            sa.move_mouse(x, y, duration)
            st.success(f"Moved mouse to ({x}, {y})")
        except Exception as e:
            st.exception(e)
    if st.button("Click Mouse"):
        try:
            sa.click(x, y)
            st.success(f"Clicked at ({x}, {y})")
        except Exception as e:
            st.exception(e)
    st.markdown("**Symbolic State:**")
    st.json(symbolic_state.get_state())