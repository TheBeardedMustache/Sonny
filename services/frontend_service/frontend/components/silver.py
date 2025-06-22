"""
silver.py: Streamlit UI for Silver Path (Desktop Automation).
"""
import streamlit as st

def silver_ui():
    """Render the Silver Path UI for desktop automation."""
    st.header("Silver Path: Desktop Automation")
    # Dynamic import to respect frontend.app overrides in tests
    try:
        from frontend.app import SilverAutomation, symbolic_state
    except ImportError:
        from backend.core.core_agent import SilverAutomation, symbolic_state
    sa = SilverAutomation()
    x = st.number_input("X-coordinate", value=0)
    y = st.number_input("Y-coordinate", value=0)
    duration = st.number_input("Duration (seconds)", value=0.0)
    if st.button("Move Mouse"):
        with st.spinner("Moving mouse..."):
            try:
                sa.move_mouse(x, y, duration)
                st.success(f"Moved mouse to ({x}, {y})")
            except Exception as e:
                st.exception(e)
    if st.button("Click Mouse"):
        with st.spinner("Clicking mouse..."):
            try:
                sa.click(x, y)
                st.success(f"Clicked at ({x}, {y})")
            except Exception as e:
                st.exception(e)
    @st.cache_data(ttl=10)
    def get_state_cached():
        return symbolic_state.get_state()

    st.subheader("Symbolic State")
    st.json(get_state_cached())