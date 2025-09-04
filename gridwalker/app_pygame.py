import time
from pathlib import Path
from .model.state import GameState
from .view.pygame3d import Pygame3DRenderer
from .controller.pygame_keys import PygameKeyboardController
from .config_store.json_store import JsonConfigStore

def run() -> None:
    cfg_path = Path.home() / '.gridwalker.json'
    cfg = JsonConfigStore(cfg_path).load()

    state = GameState(cfg=cfg, x=cfg.width // 2, y=cfg.height // 2)
    renderer = Pygame3DRenderer()
    controller = PygameKeyboardController()

    tick = cfg.tick_ms / 1000.0
    last = time.monotonic()

    try:
        while state.running:
            for action in controller.poll():
                state.apply(action)

            now = time.monotonic()
            if now - last >= tick:
                state.tick()
                last = now

            renderer.render(state)
    finally:
        controller.close()
        renderer.close()
