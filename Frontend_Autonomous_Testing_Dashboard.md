# Frontend Autonomous Testing Dashboard

This document describes the new **Autonomous Testing** dashboard page added to the Streamlit frontend.

## Component Location

- `services/frontend_service/frontend/components/autonomous_testing.py`

## App Registration

- Updated `services/frontend_service/frontend/app.py` to import `autonomous_testing_ui` and add
  a **Autonomous Testing** entry in the sidebar navigation.

## Page Features

- **Structured Autonomous Testing Instructions**: step-by-step guidance to initialize the test
  environment, run smoke and integration tests, generate coverage reports, and review results.
- **Run Full Test Suite** button: placeholder UI element to trigger the full testing pipeline.

## Usage

1. Rebuild and restart the frontend container:
   ```bash
   docker-compose build frontend_service
   docker-compose up -d frontend_service
   ```
2. Open `http://localhost:8501` in your browser.
3. Select **Autonomous Testing** from the sidebar.
4. Follow on-screen instructions and click **Run Full Test Suite** to start tests.