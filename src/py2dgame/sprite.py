import pygame
import pkg_resources


# Mixins
from py2dgame._events import _Events
from py2dgame._motion import _Motion
from py2dgame._sensing import _Sensing, _SensingSprite
from py2dgame._looks import _LooksSprite
from py2dgame._pen import _Pen
from py2dgame._variables import _Variables
from py2dgame._operators import _Operators
from py2dgame._control import _ControlSprite
from py2dgame. _sound import _Sound


class CoreSprite(_Motion, _Events, _LooksSprite, _Sound, _Sensing, _SensingSprite, _ControlSprite, _Operators, _Variables, _Pen):

    def __init__(self, stage, costume="default"):
        self.stage = stage
        # Above attributes need to be set first so that mixins can access them properly
        super().__init__()
        default_file = pkg_resources.resource_filename("py2dgame", "images/zombie_idle.png")
        self.image = pygame.image.load(default_file)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        if costume:
            self.py2dgame_addcostume(costume)
            self.name = "Sprite" if costume=="default" else costume 
        else:
            self.name = "Sprite"
        # The facade is the translated API
        self.facade = None


    def py2dgame_setname(self, name):
        self.name = name


    def update(self, dt):
        self.code_manager._update(dt)
        self.costume_manager.update_sprite_image()
        self._update_pen()


    def __str__(self):
        return self.name
