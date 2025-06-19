# Home_Page.py: Defines the homepage component for the Sonny frontend application.

import streamlit as st

def main():
    """Entry point for the home page."""
    st.title("Sonny - Lunar Venusian Martial Regulus")
    st.subheader("Welcome to Sonny's Mercury Frontend")
    # Display symbolic resonance state
    from backend.core.core_agent import symbolic_state
    st.markdown("**Symbolic State:**")
    st.json(symbolic_state.get_state())
    st.markdown(
        """
Use the sidebar to select an automation path:
- **Mercury**: Frontend interface
- **Silver**: Desktop Automation
- **Gold**: Autonomous Coding
- **Cinnabar**: Natural Language Understanding
- **Combined**: Full Automation Workflow
"""
    )

if __name__ == '__main__':
    main()

if __name__ == '__main__':
    main()