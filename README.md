# Gridwalker — an MVC example project (Python 3.11+)

A tiny, dependency-free demo game that showcases clean **MVC**, **input abstraction**, and **config storage strategies**.
Move the `@` character around a grid using **W/A/S/D**. Press **P** to pause, **Q** to quit.

## Why this design?
- **Model** holds game rules and state (no I/O). Easy to unit-test.
- **View** renders a `GameState` (here: a minimal terminal renderer).
- **Controller** turns device events (keyboard, gamepad later) into **Actions**.
- **ConfigStore** demonstrates the Strategy pattern (JSON/INI backends).

## Quick start
```bash
uv pip install -e .   # or: pip install -e .
gridwalker            # runs the game
```

## Run tests
```bash
pytest
```

## Project layout
```text
gridwalker/
    actions.py           # Action enum (device-agnostic)
    app.py               # Orchestration/game loop
    model/
        config.py          # GameConfig dataclass
        state.py           # GameState + pure update logic
    view/
        base.py            # Renderer ABC
        terminal.py        # TerminalRenderer
    controller/
        base.py            # InputDevice ABC
        keyboard.py        # Cross-platform keyboard controller
    config_store/
        base.py            # ConfigStore ABC
        json_store.py      # JSON strategy
        ini_store.py       # INI strategy
tests/
    test_state.py
```

## possible next steps
- Add **PS/Xbox controllers** by implementing `InputDevice.poll()` for those devices.
- Add a second **Renderer** (e.g., pygame) without touching the `Model`.
- Add **obstacles** or **goals** to practice pure model logic & tests.
- Swap JSON for INI via a single line in `app.py` (Strategy pattern).