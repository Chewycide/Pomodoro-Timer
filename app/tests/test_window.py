import pytest
from app.build.window import Pomodoro


@pytest.fixture
def app(qtbot):
    """Arrange/Prepare Pomodoro app for testing"""
    pomodoro = Pomodoro()
    qtbot.addWidget(pomodoro)
    return pomodoro


def test_time_to_string(app: Pomodoro):
    
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


def test_start_resume(app: Pomodoro):

    app.isPaused = False
    app.start()
    assert app.stop_btn.isEnabled() == True
    assert app.study_time_btn.isEnabled() == False
    assert app.short_break_btn.isEnabled() == False
    assert app.long_break_btn.isEnabled() == False
    assert app.run == True


def test_pause(app: Pomodoro):

    app.isPaused = True
    app.start()
    assert app.run == False


def test_timer_logic(app: Pomodoro):

    app.current_time = -1
    app.display_time()
    assert app.run == False