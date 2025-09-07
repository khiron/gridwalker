import time
from gridwalker.controller.base import InputDevice
from gridwalker.view.base import Renderer
from gridwalker.config_store.base import ConfigStore
from .state import GameState

class GridWalker:

    def __init__(self, store: ConfigStore) -> None:
        ''' Initialize the GridWalker model with configuration from the given store. '''
        self.config = store.load()
        self.save_configuration = store.save
        self.state = GameState(cfg=self.config, x=self.config.width // 2, y=self.config.height // 2)

    def run(self, view: Renderer, controller: InputDevice) -> None:
        ''' Run the main loop with the given view and controller. '''
        tick = self.config.tick_ms / 1000.0
        last = time.monotonic()

        try:
            while self.state.running:
                for action in controller.poll():
                    self.state.apply(action)

                now = time.monotonic()
                if now - last >= tick:
                    self.state.tick()
                    last = now

                view.render(self.state)
                time.sleep(0.016) # limit the fastest screen refresh to 60hz
        finally:
            controller.close()
            view.close()
            self.save_configuration(self.state.cfg)
