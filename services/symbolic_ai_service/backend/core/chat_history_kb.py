"""
Chat History Knowledge Base Loader/Interface
Loads Nick_and_Caelus_chat_history/conversations.json and provides relevant context retrieval.
"""
import os
import json
import datetime
from typing import List, Dict, Any, Tuple

CHAT_HISTORY = os.path.join(os.path.dirname(__file__), '../../../../Nick_and_Caelus_chat_history/conversations.json')

def load_conversation_history() -> List[Dict[str, Any]]:
    """Flatten all user/assistant messages into chronological list with meta."""
    if not os.path.isfile(CHAT_HISTORY):
        return []
    with open(CHAT_HISTORY, 'r', encoding='utf-8') as f:
        convs = json.load(f)
    messages = []
    for conv in convs:
        title = conv.get('title', '')
        mapping = conv.get('mapping', {})
        # Find roots and traverse
        def extract_messages(node_id, mapping, parent_title):
            node = mapping.get(node_id)
            if node is None:
                return []
            msg_obj = node.get('message')
            out = []
            if msg_obj and msg_obj.get('content') and msg_obj['content']['content_type'] == 'text':
                role = msg_obj.get('author', {}).get('role', 'unknown')
                content = ''.join(msg_obj['content'].get('parts', []))
                ts = msg_obj.get('create_time', None)
                out.append({'role': role, 'content': content, 'conversation': parent_title, 'timestamp': ts})
            # Recurse children
            for cid in node.get('children', []):
                out += extract_messages(cid, mapping, parent_title)
            return out
        for node_id in mapping:
            node = mapping[node_id]
            if node.get('parent') is None:
                out = extract_messages(node_id, mapping, title)
                messages += out
    # Sort by timestamp where possible
    messages.sort(key=lambda m: m.get('timestamp') or 0)
    return messages

def search_context(query: str, n=3) -> List[Dict[str, Any]]:
    """Naive substring search in history, returns n most recent relevant message dicts."""
    msgs = load_conversation_history()
    found = [m for m in msgs if query.lower() in m['content'].lower()]
    found = sorted(found, key=lambda m: m.get('timestamp') or 0, reverse=True)
    return found[:n]

def last_n_turns(n=5) -> List[Dict[str, Any]]:
    msgs = load_conversation_history()
    return msgs[-n:] if n > 0 else []
