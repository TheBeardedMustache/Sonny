# Home_Page.py: Defines the homepage component for the Sonny frontend application.
# Ensure frontend package imports resolve
# fallback to relative 'components' import when running via `streamlit run` in this dir
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))
try:
    from frontend.components.home import home_page
except ModuleNotFoundError:
    from components.home import home_page

def main():
    """Render the home page using purified component."""
    home_page()

if __name__ == '__main__':
    main()