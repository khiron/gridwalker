import pygame
from .base import Renderer
from gridwalker.model.state import GameState

class Pygame3DRenderer(Renderer):
    def __init__(self, width_px: int = 960, height_px: int = 720, title: str = "Gridwalker 3D"):
        pygame.init()
        self.screen = pygame.display.set_mode((width_px, height_px))
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 24)
        self.tile_w = 64
        self.tile_h = 32
        self.origin_x = width_px // 2
        self.origin_y = 100
        self.bg = (12, 12, 20)
        self.grid_top = (40, 60, 90)
        self.player_top = (220, 220, 90)
        self.player_left = (180, 180, 60)
        self.player_right = (160, 160, 50)
        self.text = (220, 220, 220)

    def _iso(self, i: int, j: int):
        x = (i - j) * (self.tile_w // 2)
        y = (i + j) * (self.tile_h // 2)
        return self.origin_x + x, self.origin_y + y

    def _diamond(self, cx, cy, w, h):
        return [
            (cx, cy),
            (cx + w//2, cy + h//2),
            (cx, cy + h),
            (cx - w//2, cy + h//2),
        ]

    def _draw_tile(self, i: int, j: int):
        cx, cy = self._iso(i, j)
        top = self._diamond(cx, cy, self.tile_w, self.tile_h)
        pygame.draw.polygon(self.screen, self.grid_top, top, width=1)

    def _draw_player_cube(self, i: int, j: int, height: int = 28):
        cx, cy = self._iso(i, j)
        top = self._diamond(cx, cy - height, self.tile_w, self.tile_h)
        right = [top[1], (top[1][0], top[1][1] + height), (top[2][0], top[2][1] + height), top[2]]
        left  = [top[3], (top[3][0], top[3][1] + height), (top[2][0], top[2][1] + height), top[2]]
        pygame.draw.polygon(self.screen, self.player_right, right)
        pygame.draw.polygon(self.screen, self.player_left, left)
        pygame.draw.polygon(self.screen, self.player_top, top)
        pygame.draw.polygon(self.screen, (0,0,0), top, width=1)

    def render(self, state: GameState) -> None:
        self.screen.fill(self.bg)
        for j in range(state.cfg.height):
            for i in range(state.cfg.width):
                self._draw_tile(i, j)
        self._draw_player_cube(state.x, state.y)
        t = f"Gridwalker 3D — pos=({state.x},{state.y}) {'[PAUSED]' if state.paused else ''}"
        self.screen.blit(self.font.render(t, True, self.text), (20, 20))
        pygame.display.flip()
        self.clock.tick(60)

    def close(self) -> None:
        pygame.quit()
