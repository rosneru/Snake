from color import Color
from game_object import GameObject
from sprite_sheet import SpriteSheet
from pygame.surface import Surface
import pygame.draw


class GameObjectStateBar(GameObject):
    def __init__(self, screen: Surface, sheet: SpriteSheet):
        self.screen = screen
        self.sheet = sheet

        self.cherry_gray = sheet.get_frames()[10]
        self.cherry_colored = sheet.get_frames()[15]

        self.width = screen.get_width()
        self.height = self.cherry_gray.get_height()
        self.top = screen.get_height() - self.height

        self.num_gray_cherries = 0
        self.num_red_cherries = 0

    def set_num_collected_cherries(self, num_gray: int, num_red: int = 0):
        self.num_gray_cherries = num_gray
        self.num_red_cherries = num_red

    def render(self):
        pygame.draw.line(
            self.screen, Color.WHITE, (0, self.top), (self.width, self.top))
        for i in range(0, 10):
            x = i * 64
            if i+1 <= self.num_red_cherries:
                self.screen.blit(self.cherry_colored, (x, self.top))
            elif i+1 <= self.num_gray_cherries:
                self.screen.blit(self.cherry_gray, (x, self.top))
            else:
                break
