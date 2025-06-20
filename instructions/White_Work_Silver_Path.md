# White Work: Purified Silver Path Instructions
This document details the refined Streamlit frontend modularization and symbolic interface enhancements.

## Modular UI Components
Located in `frontend/components/`:
- `home.py`: Home page with expandable symbolic state viewer.
- `silver.py`: Desktop Automation UI with dual-column controls and expandable state.
- `gold.py`: Autonomous Coding UI with symbolic state expander.
- `cinnabar.py`: NLU UI with symbolic state expander.
- `combined.py`: Full workflow UI with proactive task generation and state viewer.

## Adaptive Interactions
- Controls are organized into columns for clarity.
- **Symbolic State** is displayed within an expander for unobtrusive insight.
- Proactive tasks can be generated via the **Combined** UI.

## Usage Example
```bash
streamlit run frontend/app.py
```
Navigate via the sidebar and click the **Symbolic State** expander to see real-time reasoning.

## Maintenance & Reuse
- Update individual component under `frontend/components/` when refining UI.
- Tests for UI behavior are in `tests/` and should be updated accordingly.