import os
from typing import Iterable, List
from .base import InputDevice
from gridwalker.actions import Action

if os.name == 'nt':
    import msvcrt # Windows-specific

    class KeyboardController(InputDevice):
        def poll(self) -> Iterable[Action]:
            actions: List[Action] = []
            while msvcrt.kbhit():
                ch = msvcrt.getch()
                try:
                    key = ch.decode('utf-8').lower()
                except Exception:
                    continue
                if key == 'w':
                    actions.append(Action.MOVE_UP)
                elif key == 's':
                    actions.append(Action.MOVE_DOWN)
                elif key == 'a':
                    actions.append(Action.MOVE_LEFT)
                elif key == 'd':
                    actions.append(Action.MOVE_RIGHT)
                elif key == 'p':
                    actions.append(Action.PAUSE)
                elif key == 'q':
                    actions.append(Action.QUIT)
            return actions

        def close(self) -> None:
            pass

else:
    import sys, termios, tty, select

    class KeyboardController(InputDevice):
        def __init__(self) -> None:
            self._fd = sys.stdin.fileno()
            self._old = termios.tcgetattr(self._fd) # Save old terminal settings
            tty.setcbreak(self._fd) # Set terminal to cbreak mode where characters are available immediately rather than after 'enter'

        def poll(self) -> Iterable[Action]:
            actions: List[Action] = []
            if select.select([sys.stdin], [], [], 0)[0]:
                ch = sys.stdin.read(1).lower()
                if ch == 'w':
                    actions.append(Action.MOVE_UP)
                elif ch == 's':
                    actions.append(Action.MOVE_DOWN)
                elif ch == 'a':
                    actions.append(Action.MOVE_LEFT)
                elif ch == 'd':
                    actions.append(Action.MOVE_RIGHT)
                elif ch == 'p':
                    actions.append(Action.PAUSE)
                elif ch == 'q':
                    actions.append(Action.QUIT)
            return actions

        def close(self) -> None:
            termios.tcsetattr(self._fd, termios.TCSADRAIN, self._old) # Restore terminal settings
