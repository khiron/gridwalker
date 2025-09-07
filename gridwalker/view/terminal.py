import sys
from gridwalker.model.state import GameState
from .base import Renderer

def _clear():
    sys.stdout.write("\x1b[2J\x1b[H")

class TerminalRenderer(Renderer):
    def render(self, state: GameState) -> None:
        _clear()
        print(f"Gridwalker  —  position=({state.x},{state.y})  "
              f"{'[PAUSED]' if state.paused else ''}\n")
        for j in range(state.cfg.height):
            row = []
            for i in range(state.cfg.width):
                row.append('@' if (i == state.x and j == state.y) else '·')
            print(''.join(row))
        print("\nW/A/S/D to move, P pause, Q quit")

    def close(self) -> None:
        pass
