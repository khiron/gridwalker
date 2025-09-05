from abc import ABC, abstractmethod
from typing import Iterable
from ..actions import Action

class InputDevice(ABC):
    @abstractmethod
    def poll(self) -> Iterable[Action]: ...
    '''Poll the input device for new actions.'''
    @abstractmethod
    def close(self) -> None: ...
    '''Close the input device and clean up resources.'''
