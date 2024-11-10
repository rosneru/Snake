from game_object_block import GameObjectBlock
from collections import deque
from color import Color
from game_object import GameObject
from move_direction import MoveDirection
from pygame.rect import Rect
from pygame.surface import Surface


class GameObjectSnake(GameObject):
    def __init__(self,
                 screen: Surface,
                 canvas_rect: Rect,
                 head_x: int,
                 head_y: int,
                 num_limbs: int = 4,
                 move_direction: MoveDirection = MoveDirection.LEFT,
                 block_size: int = 16):
        self.screen = screen
        self.canvas_rect = canvas_rect
        self.block_size = block_size
        self.move_direction = move_direction
        self.num_blocks_x = canvas_rect.width // block_size
        self.num_blocks_y = canvas_rect.height // block_size
        self.color_head = Color.RED
        self.color_body = Color.BLUE
        self.color_inserted = Color.WHITE

        self.num_limbs_to_insert = -1

        # Create queue for limbs
        self.limbs: deque[GameObjectBlock] = deque()
        self.append_limbs(num_limbs, head_x, head_y)

    def render(self):
        for block in self.limbs:
            block.render()

    def insert_limbs(self, count: int):
        self.num_limbs_to_insert = count

    def append_limbs(self, count: int, start_x: int = -1, start_y: int = -1):
        appending_move_direction = self.move_direction
        if len(self.limbs) > 0:
            last_limb = self.limbs[-1]
            appending_move_direction = last_limb.orientation

        if start_x < 1 and start_y < 1:
            last_limb = self.limbs[-1]
            match appending_move_direction:
                case MoveDirection.LEFT:
                    start_x = last_limb.rect.x + self.block_size
                    start_y = last_limb.rect.y
                case MoveDirection.RIGHT:
                    start_x = last_limb.rect.x - self.block_size
                    start_y = last_limb.rect.y
                case MoveDirection.UP:
                    start_x = last_limb.rect.x
                    start_y = last_limb.rect.y + self.block_size
                case MoveDirection.DOWN:
                    start_x = last_limb.rect.x
                    start_y = last_limb.rect.y - self.block_size

        match appending_move_direction:
            case MoveDirection.LEFT:
                for i in range(0, count):
                    new_x = start_x + i * self.block_size
                    if new_x >= self.canvas_rect.width:
                        new_x -= self.canvas_rect.width
                    self.limbs.append(GameObjectBlock(self.screen,
                                                      new_x,
                                                      start_y,
                                                      self.color_body,
                                                      self.block_size,
                                                      self.num_blocks_x,
                                                      MoveDirection.LEFT))
            case MoveDirection.RIGHT:
                for i in range(0, count):
                    new_x = start_x - i * self.block_size
                    if new_x < 0:
                        new_x = self.canvas_rect.width + new_x
                    self.limbs.append(GameObjectBlock(self.screen,
                                                      new_x,
                                                      start_y,
                                                      self.color_body,
                                                      self.block_size,
                                                      self.num_blocks_x,
                                                      MoveDirection.RIGHT))
            case MoveDirection.UP:
                for i in range(0, count):
                    new_y = start_y + i * self.block_size
                    if new_y >= self.canvas_rect.height:
                        new_y -= self.canvas_rect.height
                    self.limbs.append(GameObjectBlock(self.screen,
                                                      start_x,
                                                      new_y,
                                                      self.color_body,
                                                      self.block_size,
                                                      self.num_blocks_x,
                                                      MoveDirection.UP))
            case MoveDirection.DOWN:
                for i in range(0, count):
                    new_y = start_y - i * self.block_size
                    if new_y < 0:
                        new_y = self.canvas_rect.height + new_y
                    self.limbs.append(GameObjectBlock(self.screen,
                                                      start_x,
                                                      new_y,
                                                      self.color_body,
                                                      self.block_size,
                                                      self.num_blocks_x,
                                                      MoveDirection.DOWN))

    def is_collision_self(self) -> bool:
        head = self.limbs[0]
        for i in range(1, len(self.limbs)):
            limb = self.limbs[i]
            if head.rect.colliderect(limb.rect):
                return True
        return False

    def move_left(self):
        # Prevent moving into the opposite direction
        if self.move_direction is MoveDirection.RIGHT:
            self.move_right()
            return

        self.move_direction = MoveDirection.LEFT

        first_limb = self._process_head_move()

        # Create the new (snake head) item at the left of the currently first
        # one
        new_limb = GameObjectBlock(self.screen,
                                   first_limb.rect.x - self.block_size,
                                   first_limb.rect.y,
                                   self.color_head,
                                   self.block_size,
                                   self.num_blocks_x,
                                   MoveDirection.LEFT)

        if new_limb.rect.x < 0:
            new_limb.rect.x = self.canvas_rect.width - self.block_size

        # Add the new item item at the beginning of the queue
        self.limbs.appendleft(new_limb)

    def move_right(self):
        # Prevent moving into the opposite direction
        if self.move_direction is MoveDirection.LEFT:
            self.move_left()
            return

        self.move_direction = MoveDirection.RIGHT

        first_limb = self._process_head_move()

        # Create the new (snake head) item at the right of the currently first
        # one
        new_limb = GameObjectBlock(self.screen,
                                   first_limb.rect.x + self.block_size,
                                   first_limb.rect.y,
                                   self.color_head,
                                   self.block_size,
                                   self.num_blocks_x,
                                   MoveDirection.RIGHT)

        if new_limb.rect.x >= self.canvas_rect.width:
            new_limb.rect.x = 0

        # Add the new item item at the beginning of the queue
        self.limbs.appendleft(new_limb)

    def move_up(self):
        # Prevent moving into the opposite direction
        if self.move_direction is MoveDirection.DOWN:
            self.move_down()
            return

        self.move_direction = MoveDirection.UP

        first_limb = self._process_head_move()

        # Create the new (snake head) item above of the currently first one
        new_limb = GameObjectBlock(self.screen,
                                   first_limb.rect.x,
                                   first_limb.rect.y - self.block_size,
                                   self.color_head,
                                   self.block_size,
                                   self.num_blocks_x,
                                   MoveDirection.UP)

        if new_limb.rect.y < 0:
            new_limb.rect.y = self.canvas_rect.height - self.block_size

        # Add the new item item at the beginning of the queue
        self.limbs.appendleft(new_limb)

    def move_down(self):
        # Prevent moving into the opposite direction
        if self.move_direction is MoveDirection.UP:
            self.move_up()
            return

        self.move_direction = MoveDirection.DOWN

        first_limb = self._process_head_move()

        # Create the new (snake head) item below the currently first one
        new_limb = GameObjectBlock(self.screen,
                                   first_limb.rect.x,
                                   first_limb.rect.y + self.block_size,
                                   self.color_head,
                                   self.block_size,
                                   self.num_blocks_x,
                                   MoveDirection.DOWN)

        if new_limb.rect.y >= self.canvas_rect.height:
            new_limb.rect.y = 0

        # Add the new item item at the beginning of the queue
        self.limbs.appendleft(new_limb)

    def move(self):
        match self.move_direction:
            case MoveDirection.LEFT:
                self.move_left()
            case MoveDirection.RIGHT:
                self.move_right()
            case MoveDirection.UP:
                self.move_up()
            case MoveDirection.DOWN:
                self.move_down()

        if self.num_limbs_to_insert > 0:
            self.num_limbs_to_insert -= 1
        elif self.num_limbs_to_insert == 0:
            # Reset the color of the latest inserted limbs to body color
            self.num_limbs_to_insert = -1
            for limb in self.limbs:
                if limb.color is self.color_head:
                    continue
                elif limb.color is self.color_inserted:
                    limb.color = self.color_body

    def _process_head_move(self) -> GameObjectBlock:
        # Depending on if there's an insert operation working or if it's just a
        # normal movement set the color of the former head limb accordingly.
        first_limb = self.limbs[0]
        if self.num_limbs_to_insert > 0:
            first_limb.color = self.color_inserted
        else:
            first_limb.color = self.color_body
            # pop() Not done when inserting (see above) as then the snake grows
            self.limbs.pop()

        return first_limb
