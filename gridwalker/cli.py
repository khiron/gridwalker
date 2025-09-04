import argparse
import importlib.util
from pathlib import Path

from .config_store.json_store import JsonConfigStore
from .model.state import GameState
from .view.terminal import TerminalRenderer
from .controller.keyboard import KeyboardController
from .view.pygame3d import Pygame3DRenderer
from .controller.pygame_keys import PygameKeyboardController

def _run_terminal() -> None:
    cfg_path = Path.home() / '.gridwalker.json'
    cfg = JsonConfigStore(cfg_path).load()
    state = GameState(cfg=cfg, x=cfg.width // 2, y=cfg.height // 2)
    renderer = TerminalRenderer()
    controller = KeyboardController()
    import time
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
            time.sleep(0.016)
    finally:
        controller.close()
        renderer.close()

def _run_pygame() -> None:
    cfg_path = Path.home() / '.gridwalker.json'
    cfg = JsonConfigStore(cfg_path).load()
    state = GameState(cfg=cfg, x=cfg.width // 2, y=cfg.height // 2)
    renderer = Pygame3DRenderer()
    controller = PygameKeyboardController()
    import time
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

def main(argv=None) -> None:
    parser = argparse.ArgumentParser(description="Gridwalker — MVC demo")
    parser.add_argument("--view", choices=["auto", "terminal", "pygame"], default="auto",
                        help="Default: auto (pygame if installed, else terminal).")
    args = parser.parse_args(argv)
    if args.view == "pygame":
        _run_pygame()
        return
    if args.view == "terminal":
        _run_terminal()
        return
    has_pygame = importlib.util.find_spec("pygame") is not None
    if has_pygame:
        _run_pygame()
    else:
        print("pygame not found — falling back to terminal view. "
              "Install with: pip install '.[pygame]' (quote on zsh).")
        _run_terminal()
