from abc import ABC, abstractmethod
from typing import Iterable
from ..actions import Action

class InputDevice(ABC):
    @abstractmethod
    def poll(self) -> Iterable[Action]: ...
    @abstractmethod
    def close(self) -> None: ...
