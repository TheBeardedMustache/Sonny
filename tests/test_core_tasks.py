from backend.core.core_tasks import handle_task

def test_handle_task_returns_none():
    assert handle_task("sample_task") is None