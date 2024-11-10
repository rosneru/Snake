from game_object_block import GameObjectBlock
from color import Color
from game_object import GameObject
from random import randrange
from pygame.rect import Rect
from pygame.surface import Surface


class GameObjectWorld(GameObject):
    def __init__(self,
                 screen: Surface,
                 canvas_rect: Rect,
                 block_size: int):
        self.screen = screen
        self.canvas_rect = canvas_rect
        self.block_size = block_size
        self.num_blocks_x = canvas_rect.width // block_size
        self.num_blocks_y = canvas_rect.height // block_size
        self.num_blocks = self.num_blocks_x * self.num_blocks_y
        self.collectible_items: list[GameObject] = []

    def render(self):
        for item in self.collectible_items:
            item.render()

    def add_collectible_item(self, used_blocks: list):
        block_id = randrange(0, self.num_blocks)
        while block_id in used_blocks:
            block_id = randrange(0, self.num_blocks)

        x = (block_id // self.num_blocks_x) * self.block_size
        y = (block_id % self.num_blocks_y) * self.block_size
        block = GameObjectBlock(
            self.screen, x, y, Color.PURPLE, self.block_size, self.num_blocks_x)
        self.collectible_items.append(block)

    def remove_collectible_item(self, block_id):
        item_to_remove = -1
        for i in range(0, len(self.collectible_items)):
            if self.collectible_items[i].block_id == block_id:
                item_to_remove = i
                break

        if item_to_remove >= 0:
            del self.collectible_items[item_to_remove]
