"""
combined.py: Streamlit UI for Combined Path (Full Workflow).
"""
import streamlit as st
from backend.core.core_agent import symbolic_state

def combined_ui():
    """Render the Combined Path UI for end-to-end workflows."""
    st.header("Combined Path: Full Workflow")
    st.write("Generate and execute tasks in a unified workflow.")
    st.markdown("**Symbolic State:**")
    st.json(symbolic_state.get_state())
    # Proactive task generation
    from backend.core.core_agent import AnimatedMercury
    am = AnimatedMercury(symbolic_state=symbolic_state)
    if st.button("Generate Proactive Task"):
        try:
            task = am.generate_proactive_task()
            st.success("Proactive Task Generated:")
            st.code(task, language="python")
        except Exception as e:
            st.exception(e)