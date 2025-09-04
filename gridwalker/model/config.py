from dataclasses import dataclass

@dataclass(frozen=True)
class GameConfig:
    width: int = 20
    height: int = 12
    tick_ms: int = 100
