from pathlib import Path
import typer # simple CLI library built on Click that supports type hints

from .controller.keyboard import KeyboardController
from .controller.pygame_keys import PygameKeyboardController
from .model.gridwalker import GridWalker
from .view.pygame3d import Pygame3DRenderer
from .view.terminal import TerminalRenderer
from .config_store.base import ConfigStore
from .config_store.json_store import JsonConfigStore
from .config_store.ini_store import IniConfigStore

app = typer.Typer(add_completion=False, help="Gridwalker — MVC demo")

def _make_store(backend: str) -> ConfigStore:
    home = Path.home()
    if backend.lower() == "ini":
        return IniConfigStore(home / ".gridwalker.ini")
    return JsonConfigStore(home / ".gridwalker.json")

@app.command()
def main(
    view: str = typer.Option(
        "terminal", # default option 
        "--view",
        "-v",
        help="Which view to run: terminal | pygame",
        metavar="VIEW",
        show_default=True,
    ),
    config_backend: str = typer.Option(
        "json",
        "--config-backend",
        "-c",
        help="Where to store config: json | ini",
        metavar="BACKEND",
        show_default=True,
    ),
) -> None:
    """ Run Gridwalker. By default it will choose a terminal mode game board and W/A/S/D keyboard controls."""
    store = _make_store(config_backend) # a config store uses the strategy pattern
    model = GridWalker(store) # use Dependency Injection (DI) to give the model a strategy for persisting configuration    
    v = view.lower()
    if v == "terminal":
        model.run(view=TerminalRenderer(), controller=KeyboardController()) # use Dependency Injection to pass the view and controller to the model
    elif v == "pygame":
        model.run(view=Pygame3DRenderer(), controller=PygameKeyboardController())

if __name__ == "__main__": # if run as a script then run the CLI
    app()