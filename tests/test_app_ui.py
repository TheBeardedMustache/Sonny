"""Tests for frontend app UI functions exist and import correctly."""
import pytest

import frontend.app as app

def test_app_ui_functions_exist():
    assert hasattr(app, 'main')
    assert hasattr(app, 'silver_ui')
    assert hasattr(app, 'gold_ui')
    assert hasattr(app, 'cinnabar_ui')
    assert hasattr(app, 'combined_ui')