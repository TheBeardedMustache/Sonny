# Reusable Frontend Modules
This document describes modular frontend components for reuse.

## Components Directory Structure
- `frontend/components/`
  - `home.py`: Home page UI (`home_page()`)
  - `silver.py`: Silver Path UI (`silver_ui()`)
  - `gold.py`: Gold Path UI (`gold_ui()`)
  - `cinnabar.py`: Cinnabar Path UI (`cinnabar_ui()`)
  - `combined.py`: Combined Path UI (`combined_ui()`)

## Usage
Import and call the respective UI function in your Streamlit app:
```python
import streamlit as st
from frontend.components.silver import silver_ui

def main():
    st.sidebar.title("Sonny Navigation")
    choice = st.sidebar.radio("Choose Path", ["Silver"])
    if choice == "Silver":
        silver_ui()

if __name__ == '__main__':
    main()
```

## Maintenance
When refining UI flows, update the corresponding file under `components/`.
Remove redundant logic from `app.py` to keep it lightweight and maintain clear separation of concerns.