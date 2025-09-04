from abc import ABC, abstractmethod
from ..model.state import GameState

class Renderer(ABC):
    @abstractmethod
    def render(self, state: GameState) -> None: ...
    @abstractmethod
    def close(self) -> None: ...
