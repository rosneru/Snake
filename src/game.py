from collections import deque
from enum import Enum
from transitions import Machine, State
from pygame.surface import Surface
from pygame.rect import Rect
import os

from color import Color
from game_object import GameObject
from game_object_snake import GameObjectSnake
from game_object_state_bar import GameObjectStateBar
from game_object_world import GameObjectWorld
from move_direction import MoveDirection
from pictures import CrashPicture, SuccessPicture
from sprite_sheet import SpriteSheet


class Game:
    class States(Enum):
        CREATE_LEVEL = 0
        RUN = 1
        SHOW_ADDED = 2
        SHOW_CRASH = 3
        SHOW_WIN = 4
        DELAY = 5

    states = [
        State(States.CREATE_LEVEL, on_enter='init_state_create_level'),
        State(States.RUN, on_enter='init_state_run'),
        State(States.SHOW_ADDED, on_enter='init_state_show_added'),
        State(States.SHOW_CRASH, on_enter='init_state_show_crash'),
        State(States.SHOW_WIN, on_enter='init_state_show_win'),
        State(States.DELAY, on_enter='init_state_delay'),
    ]

    transitions = [
        ['enter_state_create_level', States.DELAY, States.CREATE_LEVEL],
        ['enter_state_run', States.CREATE_LEVEL, States.RUN],
        ['enter_state_show_added', States.RUN, States.SHOW_ADDED],
        ['enter_state_run', States.SHOW_ADDED, States.RUN],
        ['enter_state_show_crash', States.RUN, States.SHOW_CRASH],
        ['enter_state_show_win', States.RUN, States.SHOW_WIN],
        ['enter_state_delay', States.SHOW_CRASH, States.DELAY],
        ['enter_state_delay', States.SHOW_WIN, States.DELAY],
    ]

    def __init__(self, screen: Surface, block_size):
        self.screen = screen
        self.block_size = block_size

        self.machine = Machine(model=self,
                               states=Game.states,
                               transitions=Game.transitions,
                               initial=Game.States.CREATE_LEVEL)
        self.state_tick_counter = 0
        self.state: Game.States
        sheet_image = os.path.join('../gfx', 'snake-graphics.png')
        sheet = SpriteSheet(sheet_image, 4, 5)
        self.cherry_colored = sheet.get_frames()[15]
        self.state_bar = GameObjectStateBar(self.screen, sheet)
        self.canvas_rect = Rect(
            0, 0, self.screen.get_width(),
            self.screen.get_height() - self.state_bar.height)
        self.num_total_cherries = 0
        self.num_collected_cherries = 0
        self.game_objects: list[GameObject] = []
        self.game_objects.append(self.state_bar)
        self.crash_picture = CrashPicture(self.screen, self.block_size)
        self.winning_picture = SuccessPicture(self.screen, self.block_size)
        self.speed: int = 10
        self.former_speed: int = 10
        self.is_temp_speed_active = False

    def get_speed(self) -> int:
        return self.speed

    def set_speed(self, speed: int):
        if self.is_temp_speed_active:
            return
        self.speed = speed

    def set_temp_speed(self, speed: int):
        self.former_speed = self.speed
        self.speed = speed
        self.is_temp_speed_active = True

    def reset_speed(self):
        if not self.is_temp_speed_active:
            return
        self.speed = self.former_speed
        self.is_temp_speed_active = False

    def create_level_1(self):
        self.snake = GameObjectSnake(screen=self.screen,
                                     canvas_rect=self.canvas_rect,
                                     head_x=10 * self.block_size,
                                     head_y=5 * self.block_size,
                                     num_limbs=10,
                                     move_direction=MoveDirection.LEFT,
                                     block_size=self.block_size)
        self.game_world = GameObjectWorld(self.screen,
                                          self.canvas_rect,
                                          self.block_size)
        self.direction_queue = deque()
        self.snake_collides_itself = False

        snake_used_blocks = [o.block_id for o in self.snake.limbs]
        self.game_world.add_collectible_item(snake_used_blocks)

        self.game_objects.append(self.game_world)
        self.game_objects.append(self.snake)

    def append_new_direction(self, direction: MoveDirection):
        # Don't store user key input while in 'collision with itself' state
        if self.state != Game.States.RUN:
            return

        if len(self.direction_queue) > 1:
            if self.direction_queue[-1] is not direction:
                self.direction_queue.append(direction)
        else:
            self.direction_queue.append(direction)

    def init_state_create_level(self):
        self.state_tick_counter = 0
        self.num_total_cherries = 0
        self.num_collected_cherries = 0
        self.state_bar.set_num_collected_cherries(0)
        self.game_objects.clear()
        self.game_objects.append(self.state_bar)

    def do_state_create_level(self):
        if self.num_total_cherries > 9:
            self.create_level_1()
            self.enter_state_run()
        else:
            self.num_total_cherries += 1
            self.state_bar.set_num_collected_cherries(self.num_total_cherries)

    def init_state_run(self):
        self.state_tick_counter = 0

    def do_state_run(self):
        new_move_direction = MoveDirection.NONE
        if len(self.direction_queue) > 0:
            new_move_direction = self.direction_queue.pop()
        match new_move_direction:
            case MoveDirection.NONE:
                self.snake.move()
            case MoveDirection.LEFT:
                self.snake.move_left()
            case MoveDirection.RIGHT:
                self.snake.move_right()
            case MoveDirection.UP:
                self.snake.move_up()
            case MoveDirection.DOWN:
                self.snake.move_down()
        if self.snake.is_collision_self():
            self.enter_state_show_crash()
            return

        # Check if head / limb[0] of snake collided with a collectable item
        item_blocks = [o.block_id for o in self.game_world.collectible_items]
        snake_head_block_id = self.snake.limbs[0].block_id
        if snake_head_block_id in item_blocks:
            self.game_world.remove_collectible_item(snake_head_block_id)

            snake_used_blocks = [o.block_id for o in self.snake.limbs]
            self.game_world.add_collectible_item(snake_used_blocks)

            num_new_limbs = 3
            self.snake.insert_limbs(num_new_limbs)
            self.new_limbs_idx = len(self.snake.limbs) - num_new_limbs

            self.num_collected_cherries += 1
            self.state_bar.set_num_collected_cherries(
                self.num_total_cherries, self.num_collected_cherries)

            if self.num_collected_cherries == self.num_total_cherries:
                self.enter_state_show_win()

    def init_state_show_added(self):
        self.state_tick_counter = 0

    def do_state_show_added(self):
        self.state_tick_counter += 1
        if self.state_tick_counter > 1:
            self.enter_state_run()

    def init_state_show_crash(self):
        self.state_tick_counter = 0
        self.set_temp_speed(60)
        self.game_objects.clear()

    def do_state_show_crash(self):
        if self.crash_picture.compose(self.game_objects) is True:
            self.enter_state_delay()

    def init_state_show_win(self):
        self.state_tick_counter = 0
        self.set_temp_speed(60)
        self.game_objects.clear()

    def do_state_show_win(self):
        if self.winning_picture.compose(self.game_objects) is True:
            self.enter_state_delay()

    def init_state_delay(self):
        self.state_tick_counter = 0
        self.reset_speed()

    def do_state_delay(self):
        self.state_tick_counter += 1
        if self.state_tick_counter > 10:
            self.enter_state_create_level()

    def update(self):
        match self.state:
            case Game.States.CREATE_LEVEL:
                self.do_state_create_level()
            case Game.States.RUN:
                self.do_state_run()
            case Game.States.SHOW_ADDED:
                self.do_state_show_added()
            case Game.States.SHOW_CRASH:
                self.do_state_show_crash()
            case Game.States.SHOW_WIN:
                self.do_state_show_win()
            case Game.States.DELAY:
                self.do_state_delay()

    def render(self):
        self.screen.fill(Color.BLACK)
        for game_object in self.game_objects:
            game_object.render()
