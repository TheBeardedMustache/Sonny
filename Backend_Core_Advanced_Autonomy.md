# Backend Core Advanced Autonomy

This document describes advanced proactive autonomy and predictive capabilities added to the Backend Core service to achieve Rubedo maturity.

## 1. Proactive Task Planning Endpoint (`/autonomy/proactive/`)

Allows the service to suggest next actions based on the current application or symbolic state:

```jsonc
POST /autonomy/proactive/
{ "state": { ... } }
-> { "tasks": ["proactive_task_1", "proactive_task_2"] }
```

## 2. Predictive Actions Endpoint (`/autonomy/predict/`)

Provides a prediction of likely next actions or decisions using statistical or machine‑learning methods:

```jsonc
POST /autonomy/predict/
{ "state": { ... } }
-> { "predicted_actions": ["action_a", "action_b"] }
```

## 3. Implementation Details

- Stub implementations live in `backend/core/autonomy.py`.
- Endpoints wired in `backend/api.py` with Pydantic request models.

## 4. Future Work

- Integrate ML-based forecasting for predictions.
- Connect to external planning engines for richer task plans.
- Add caching and rate limiting on autonomy endpoints.