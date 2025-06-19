import pytest

import streamlit as st

import frontend.app as app

def test_ui_functions_exist():
    assert hasattr(app, 'main')
    assert hasattr(app, 'silver_ui')
    assert hasattr(app, 'gold_ui')
    assert hasattr(app, 'cinnabar_ui')
    assert hasattr(app, 'combined_ui')

def test_home_page_importable():
    # Ensure Home_Page module can be imported and its main function exists
    import frontend.Home_Page as hp
    assert hasattr(hp, 'main')