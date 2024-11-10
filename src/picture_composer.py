from color import Color
from game_object import GameObject
from game_object_block import GameObjectBlock
from pygame.surface import Surface


class PictureComposer:
    def __init__(self,
                 screen: Surface,
                 block_size: int,
                 color: tuple,
                 image_data: list[int],
                 image_width: int):
        self.screen = screen
        self.block_size = block_size
        self.color = color
        self.image_data = image_data
        self.image_width = image_width
        self.idx = 0

    def compose(self, game_objects: list[GameObject]) -> bool:
        '''Add the next (visible, non-zero) picture pixel to the `game_objects`
         list. Returns `False` until the picture is complete. Then it returns
         `True` once and then starts building the image again from the
         beginning'''

        # Restart
        if self.idx == len(self.image_data):
            self.idx = 0

        # Fast-forward until data with a non-zero value
        while self.image_data[self.idx] == 0:
            self.idx += 1
            if self.idx == len(self.image_data):
                return True

        column = self.idx % self.image_width
        row = int(self.idx / self.image_width)
        game_objects.append(GameObjectBlock(self.screen,
                                            column * self.block_size,
                                            row * self.block_size,
                                            self.color,
                                            self.block_size,
                                            self.block_size))
        self.idx += 1
        if self.idx == len(self.image_data):
            return True
        return False
