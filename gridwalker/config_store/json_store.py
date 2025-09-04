import json
from pathlib import Path
from ..model.config import GameConfig
from .base import ConfigStore

class JsonConfigStore(ConfigStore):
    def __init__(self, path: Path) -> None:
        self.path = path

    def load(self) -> GameConfig:
        if not self.path.exists():
            return GameConfig()
        data = json.loads(self.path.read_text())
        return GameConfig(**data)

    def save(self, cfg: GameConfig) -> None:
        self.path.write_text(json.dumps(cfg.__dict__, indent=2))
