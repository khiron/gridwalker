import time
from pathlib import Path
from .model.config import GameConfig
from .model.state import GameState
from .view.terminal import TerminalRenderer
from .controller.keyboard import KeyboardController
from .config_store.json_store import JsonConfigStore

def run() -> None:
    cfg_path = Path.home() / '.gridwalker.json'
    store = JsonConfigStore(cfg_path)
    cfg = store.load()

    state = GameState(cfg=cfg, x=cfg.width // 2, y=cfg.height // 2)
    renderer = TerminalRenderer()
    controller = KeyboardController()

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
            time.sleep(0.016)  # ~60 fps cap
    finally:
        controller.close()
        renderer.close()
        store.save(state.cfg)

if __name__ == '__main__':
    run()
