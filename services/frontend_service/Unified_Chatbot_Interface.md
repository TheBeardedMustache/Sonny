## Unified Chatbot Interface

### Overview
This mode transforms the frontend into a streamlined, **chat-only interface** for interaction with Sonny.

All mouse/automation/coding controls and UI expanders are removed. Only the chat window and message log are present.

### Features
- **Chat-only UI**: One central box for chat history, and a text input for sending user messages.
- **No sidebars/tabs**: The navigation, sliders, and buttons for automation/coding are removed.
- **Logging**: Every user message and Sonny's response is appended to `services/frontend_service/logs/chat_interactions.log` in timestamped, plaintext format.

### Code Location
- Main chat interface logic: `services/frontend_service/frontend/app.py`
- Chat interaction log: `services/frontend_service/logs/chat_interactions.log`

### Expected Usage
1. Type a message in the input at the bottom and click `Send` or press `Enter`.
2. Conversation history is preserved in-session and scrolls upward.
3. Each sent/received message is appended as a new line in the log file, format:  
    `[YYYY-MM-DD HH:MM:SS] ROLE: message`

### Customization/Extension
- To handle backend processing, ensure the backend exposes `process_chat(prompt:str) -> str` in `backend.core.core_agent`.
- To change the log format/location, edit `log_chat` in `app.py`.

### Example Log
```text
[2024-06-22 14:01:17] USER: Hello Sonny!
[2024-06-22 14:01:18] SONNY: Hello human. How can I help you today?
```

---
**Deployment**: Run using:
```sh
streamlit run app.py
# or via docker-compose as usual
```