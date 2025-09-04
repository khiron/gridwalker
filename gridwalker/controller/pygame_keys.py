import pygame
from typing import Iterable, List
from .base import InputDevice
from ..actions import Action

class PygameKeyboardController(InputDevice):
    def __init__(self) -> None:
        if not pygame.get_init():
            pygame.init()

    def poll(self) -> Iterable[Action]:
        actions: List[Action] = []
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                actions.append(Action.QUIT)
            elif event.type == pygame.KEYDOWN:
                key = event.key
                if key in (pygame.K_q, pygame.K_ESCAPE):
                    actions.append(Action.QUIT)
                elif key == pygame.K_p:
                    actions.append(Action.PAUSE)
                elif key in (pygame.K_w, pygame.K_UP):
                    actions.append(Action.MOVE_UP)
                elif key in (pygame.K_s, pygame.K_DOWN):
                    actions.append(Action.MOVE_DOWN)
                elif key in (pygame.K_a, pygame.K_LEFT):
                    actions.append(Action.MOVE_LEFT)
                elif key in (pygame.K_d, pygame.K_RIGHT):
                    actions.append(Action.MOVE_RIGHT)
        return actions

    def close(self) -> None:
        pass
