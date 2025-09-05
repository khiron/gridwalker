
# Gridwalker — MVC example (Python 3.11+)

A tiny game used to show **separation of concerns** with clean architecture.
Move the `@` with **W/A/S/D**. Press **P** to pause, **Q**/Esc to quit.
Two views ship: a **terminal** view and an **isometric (3D-ish)** pygame view.

---

## Install & Run
```bash
uv pip install -e .
gridwalker                 # auto: pygame if installed, else terminal
gridwalker --view terminal # force terminal
gridwalker --view pygame   # force pygame 
```

---

## Why this design? (the patterns & why they help)

### 1) Model–View–Controller (MVC)
**Goal:** separate game **rules/state** (Model) from **rendering** (View) and **input** (Controller).

- **Model**: `gridwalker/model/state.py` holds `GameState` with pure logic (`apply()` and `tick()`).
  It never reads the keyboard or draws pixels. That makes it **easy to test** and reuse.
- **View**: `gridwalker/view/terminal.py` and `gridwalker/view/pygame3d.py` render a given `GameState`.
  You can swap views without touching the Model.
- **Controller**: `gridwalker/controller/*` turns device events into **Actions** (e.g., `MOVE_LEFT`).
  The game loop applies those actions to the Model. Views don’t know about devices, and Models don’t know about screens.

**Benefit:** Each part has one reason to change. You can teach and evolve rendering, input, or rules **independently**.

---

### 2) Strategy pattern for configuration storage
**Goal:** make *how* config is stored pluggable without changing the rest of the app.

- `ConfigStore` (interface): `gridwalker/config_store/base.py`
- Concrete strategies:
  - JSON: `gridwalker/config_store/json_store.py`
  - INI:  `gridwalker/config_store/ini_store.py`

The app chooses a strategy at composition time:

```python
# app.py
from .config_store.json_store import JsonConfigStore
store = JsonConfigStore(Path.home() / ".gridwalker.json")
cfg = store.load()
```

**Swap it:** replace the import with `IniConfigStore` and the rest of the code stays the same.

**Takeaway:** We're passing a strategy for configuration storage to the app which makes it easy to change the storage format without affecting the rest of the code.

---

### 3) Input abstraction (device → Action mapping)
**Goal:** isolate device specifics (terminal keyboard, pygame key events, future controllers) from the Model.

- `InputDevice` interface: `gridwalker/controller/base.py`
- Terminal keyboard: `gridwalker/controller/keyboard.py`
- Pygame keyboard:  `gridwalker/controller/pygame_keys.py`

Controllers return **Action** values defined in `gridwalker/actions.py`. The game loop consumes actions:

```python
for action in controller.poll():
    state.apply(action)  # pure logic
```

**Takeaway:** We can add PS/Xbox controllers later by implementing `poll()`—no Model/View changes required.

---

### 4) Testing the Model
**Goal:** make correctness checkable fast and locally.

- Tests live in `tests/` and target the **pure** Model (`GameState`), e.g. clamped movement, pause/quit.
- No I/O or graphics in tests → they run quickly and deterministically.

Run them:
```bash
pytest
```

**Takeaway:** We can write tests against **logic**, not against side effects. 
Having a collection of tests that check all our assumptions builds confidence that allows us to refactor code and know that fixing one thing doesn't break another elsewhere in the code.

---

### 5) Continuous Integration (CI)
**Goal:** run tests automatically on every push/PR in a clean environment.

- Workflow: `.github/workflows/ci.yml` any yml file in this special path is picked up by GitHub Actions and run on every push/PR.
- Uses `ubuntu-latest` with Python 3.11
- Installs the package and runs `pytest`

**Takeaway:** Testing code as part of the check-in procedure prevents “works on my machine” issues and models a professional review loop—green checks before merge.

---

## Project layout
```text
gridwalker/
  actions.py               # Action enum (device-agnostic)
  cli.py                   # 'gridwalker' entry: auto view (pygame if installed)
  app.py                   # Terminal app wiring
  app_pygame.py            # Pygame app wiring
  model/
    config.py              # GameConfig dataclass
    state.py               # GameState + pure update logic
  view/
    base.py                # Renderer ABC
    terminal.py            # TerminalRenderer
    pygame3d.py            # Isometric Pygame3DRenderer
  controller/
    base.py                # InputDevice ABC
    keyboard.py            # Terminal keyboard controller
    pygame_keys.py         # Pygame keyboard controller
  config_store/
    base.py                # ConfigStore ABC
    json_store.py          # JSON strategy
    ini_store.py           # INI strategy
tests/
  test_state.py
.github/workflows/ci.yml   # GitHub Actions tests
```

---

## Next steps you can try 
- Add collisions with obstacles & goals to the game model → extend Model + tests only.
- Add a new view (e.g., pygame top‑down or ASCII color) → implement a `Renderer`.
- Add PS/Xbox controllers → implement another `InputDevice` that returns Actions.
- Try an alternate config backend (YAML, TOML, SQLite) → new `ConfigStore` strategy.

