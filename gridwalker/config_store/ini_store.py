from configparser import ConfigParser
from pathlib import Path
from gridwalker.model.config import GameConfig
from .base import ConfigStore

class IniConfigStore(ConfigStore):
    def __init__(self, path: Path) -> None:
        self.path = path

    def load(self) -> GameConfig:
        if not self.path.exists():
            return GameConfig()
        cp = ConfigParser()
        cp.read(self.path)
        return GameConfig(
            width=cp.getint('game', 'width', fallback=20),
            height=cp.getint('game', 'height', fallback=12),
            tick_ms=cp.getint('game', 'tick_ms', fallback=100),
        )

    def save(self, cfg: GameConfig) -> None:
        cp = ConfigParser()
        cp['game'] = {
            'width': str(cfg.width),
            'height': str(cfg.height),
            'tick_ms': str(cfg.tick_ms),
        }
        with self.path.open('w') as f:
            cp.write(f)
