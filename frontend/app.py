"""app.py: Entry point for the Sonny frontend application using Streamlit."""
import os
import sys
# Ensure project root is on PYTHONPATH for absolute 'frontend' imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))
import streamlit as st

# Try absolute imports (for test environments);
# fall back to relative 'components' imports when running via `streamlit run`
try:
    from components.home import home_page
    from frontend.components.silver import silver_ui
    from frontend.components.gold import gold_ui
    from frontend.components.cinnabar import cinnabar_ui
    from frontend.components.combined import combined_ui
except ModuleNotFoundError:
    from components.home import home_page
    from components.silver import silver_ui
    from components.gold import gold_ui
    from components.cinnabar import cinnabar_ui
    from components.combined import combined_ui
# Expose core classes/functions for UI components and test overrides
from backend.core.core_agent import SilverAutomation, GoldAutomation, process_request, symbolic_state, AnimatedMercury


def main():
    st.sidebar.title("Sonny Navigation")
    choice = st.sidebar.radio(
        "Choose Path",
        ["Home", "Silver", "Gold", "Cinnabar", "Combined"],
    )
    if choice == "Home":
        home_page()
    elif choice == "Silver":
        silver_ui()
    elif choice == "Gold":
        gold_ui()
    elif choice == "Cinnabar":
        cinnabar_ui()
    elif choice == "Combined":
        combined_ui()

if __name__ == "__main__":
    main()