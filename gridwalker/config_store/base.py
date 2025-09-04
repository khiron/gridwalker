from abc import ABC, abstractmethod
from ..model.config import GameConfig

class ConfigStore(ABC):
    @abstractmethod
    def load(self) -> GameConfig: ...
    @abstractmethod
    def save(self, cfg: GameConfig) -> None: ...
