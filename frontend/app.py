# app.py: Entry point for the Sonny frontend application using Streamlit.

import streamlit as st
from frontend.components.home import home_page
from frontend.components.silver import silver_ui
from frontend.components.gold import gold_ui
from frontend.components.cinnabar import cinnabar_ui
from frontend.components.combined import combined_ui
from backend.core.core_agent import SilverAutomation, GoldAutomation, process_request, symbolic_state


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