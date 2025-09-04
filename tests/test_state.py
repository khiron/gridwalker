from gridwalker.model.config import GameConfig
from gridwalker.model.state import GameState
from gridwalker.actions import Action

def test_bounds_and_moves():
    s = GameState(GameConfig(width=3, height=2), x=1, y=1)
    s.apply(Action.MOVE_RIGHT)
    assert (s.x, s.y) == (2, 1)
    s.apply(Action.MOVE_RIGHT)
    assert (s.x, s.y) == (2, 1)
    s.apply(Action.MOVE_LEFT)
    assert (s.x, s.y) == (1, 1)
    s.apply(Action.MOVE_UP)
    assert (s.x, s.y) == (1, 0)
    s.apply(Action.MOVE_UP)
    assert (s.x, s.y) == (1, 0)
    s.apply(Action.MOVE_DOWN)
    assert (s.x, s.y) == (1, 1)

def test_pause_and_quit():
    s = GameState(GameConfig(), x=0, y=0)
    s.apply(Action.PAUSE)
    assert s.paused
    s.apply(Action.MOVE_RIGHT)  # ignored while paused
    assert (s.x, s.y) == (0, 0)
    s.apply(Action.PAUSE)
    assert not s.paused
    s.apply(Action.QUIT)
    assert not s.running
