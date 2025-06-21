# Frontend Advanced Optimization

This guide outlines strategies and Streamlit code improvements to boost responsiveness and reduce unnecessary recomputation in the frontend UI.

## 1. Cache Expensive Operations

- Use `@st.cache_data` to memoize calls to backend APIs or LLM wrappers.

Example (Cinnabar Path):
```python
@st.cache_data(ttl=300)
def interpret_cached(text: str):
    return process_request(text)

response = interpret_cached(user_input)
```

## 2. Cache Symbolic State Rendering

- Use short TTL caching on `symbolic_state.get_state()` to avoid rerendering JSON on every interaction.

```python
@st.cache_data(ttl=10)
def get_state_cached():
    return symbolic_state.get_state()

st.json(get_state_cached())
```

## 3. Reduce Reruns with Session State

- Store intermediate values in `st.session_state` to prevent controls from resetting when other widgets update.

```python
if 'prompt' not in st.session_state:
    st.session_state.prompt = ''
prompt = st.text_area('Prompt', st.session_state.prompt)
```

## 4. Optimize Layout

- Group related inputs/buttons in `st.columns` to minimize vertical layout and reduce reflow.

```python
col1, col2 = st.columns(2)
with col1:
    x = st.number_input('X')
with col2:
    y = st.number_input('Y')
```

## 5. Asynchronous Data Fetch (Future)

- Consider using `st.experimental_data_editor` or asyncio with background threads for non-blocking UI updates.

## 6. Spinner & Progress Bar Consistency

- Use informative spinner messages and optional `st.progress` for long-running tasks.

```python
with st.spinner('Working...'):
    result = heavy_operation()
    st.progress(100)
```

## 7. Lazy Loading Components

- Load heavy UI sections only when selected via sidebar radio to avoid unnecessary imports/recomputations.

```python
if choice == 'Gold':
    gold_ui()
```