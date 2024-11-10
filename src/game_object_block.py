from pygame.surface import Surface

from game_object import GameObject
from move_direction import MoveDirection
import pygame.draw

class GameObjectBlock(GameObject):
    '''
    A block which occupies an rectangular area of the game world and has a
    block id
    '''
    def __init__(self,
                 screen: Surface,
                 x: float,
                 y: float,
                 color: tuple,
                 block_size: float,
                 num_blocks_x: int,
                 orientation: MoveDirection = MoveDirection.NONE):
        self.screen: Surface = screen
        self.color = color
        self.rect = pygame.Rect(x, y, block_size-1, block_size-1)
        self.orientation = orientation

        column_id = x // block_size
        row_id = y // block_size
        self.block_id = row_id * num_blocks_x + column_id

    def render(self):
        pygame.draw.rect(self.screen, self.color, self.rect)

