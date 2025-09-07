from abc import ABC, abstractmethod
from gridwalker.model.config import GameConfig

class ConfigStore(ABC):
    @abstractmethod
    def load(self) -> GameConfig: ...
    '''Load the game configuration.'''
    @abstractmethod
    def save(self, cfg: GameConfig) -> None: ...
    '''Save the game configuration.'''
