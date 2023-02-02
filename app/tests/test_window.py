import pytest
from app.build.window import Pomodoro


@pytest.fixture
def app(qtbot):
    """Arrange/Prepare Pomodoro app for testing"""
    pomodoro = Pomodoro()
    qtbot.addWidget(pomodoro)
    return pomodoro


def test_time_to_string(app):
    
    app.current_time = 1500
    return_str = app.time_to_string()
    assert return_str == "25:00"

    app.current_time = 1400
    return_str = app.time_to_string()
    assert return_str == "23:20"

    app.current_time = 0
    return_str = app.time_to_string()
    assert return_str == "00:00"

    app.current_time = 599
    return_str = app.time_to_string()
    assert return_str == "09:59"