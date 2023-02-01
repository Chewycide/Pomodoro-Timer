from app.build.window import Pomodoro

def test_window(qtbot):
    """TODO: group tests into class"""
    pomodoro = Pomodoro()
    qtbot.addWidget(pomodoro)

    pomodoro.current_time = 1500
    return_str = pomodoro.time_to_string()
    print("test")
    assert return_str == "25:00"
