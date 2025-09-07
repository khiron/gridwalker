from dataclasses import dataclass
from .config import GameConfig
from gridwalker.actions import Action

@dataclass
class GameState:
    cfg: GameConfig
    x: int = 0
    y: int = 0
    paused: bool = False
    running: bool = True

    def apply(self, action: Action) -> None:
        if action == Action.QUIT:
            self.running = False
            return
        if action == Action.PAUSE:
            self.paused = not self.paused
            return
        if self.paused:
            return
        if action == Action.MOVE_UP:
            self.y = max(0, self.y - 1)
        elif action == Action.MOVE_DOWN:
            self.y = min(self.cfg.height - 1, self.y + 1)
        elif action == Action.MOVE_LEFT:
            self.x = max(0, self.x - 1)
        elif action == Action.MOVE_RIGHT:
            self.x = min(self.cfg.width - 1, self.x + 1)

    def tick(self) -> None:
        if not self.paused:
            pass
