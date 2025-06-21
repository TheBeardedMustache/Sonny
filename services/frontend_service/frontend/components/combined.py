"""
combined.py: Streamlit UI for Combined Path (Full Workflow).
"""
import streamlit as st

def combined_ui():
    """Render the Combined Path UI for end-to-end workflows."""
    st.header("Combined Path: Full Workflow")
    st.write("Generate and execute tasks in a unified workflow.")
    # Dynamic import to accommodate test overrides
    try:
        from frontend.app import AnimatedMercury, symbolic_state
    except ImportError:
        from backend.core.core_agent import AnimatedMercury, symbolic_state
    am = AnimatedMercury(symbolic_state=symbolic_state)
    @st.cache_data(ttl=300)
    def proactive_cached():
        return am.generate_proactive_task()

    if st.button("Generate Proactive Task"):
        with st.spinner("Generating proactive task..."):
            try:
                task = proactive_cached()
                symbolic_state.update("proactive_task", task)
                st.success("Proactive Task Generated:")
                st.code(task, language="python")
            except Exception as e:
                st.exception(e)
    @st.cache_data(ttl=10)
    def get_state_cached():
        return symbolic_state.get_state()

    st.subheader("Symbolic State")
    st.json(get_state_cached())