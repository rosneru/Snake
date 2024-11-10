import pygame
import unittest
from move_direction import MoveDirection
from game_object_snake import GameObjectSnake


class TestGameObjects(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestGameObjects, self).__init__(*args, **kwargs)

        # The following properties are used for most of the tests
        # (but currently not for the first one, test_SnakeCreation)
        canvas_width = 128
        canvas_height = 128
        self.block_size = 16
        self.canvas_rect = pygame.Rect(0, 0, canvas_width, canvas_height)
        self.screen = pygame.surface.Surface([canvas_width, canvas_height])

    def test_SnakeCreation(self):
        block_size = 16
        canvas_width = 640
        canvas_height = 512
        canvas_rect = pygame.Rect(0, 0, canvas_width, canvas_height)
        screen = pygame.surface.Surface([canvas_width, canvas_height])
        snake = GameObjectSnake(screen=screen,
                                canvas_rect=canvas_rect,
                                head_x=10 * block_size,
                                head_y=5 * block_size,
                                num_limbs=4,
                                move_direction=MoveDirection.LEFT,
                                block_size=block_size)

        self.assertEqual(len(snake.limbs), 4,
                         'New snake must have 4 limbs.')

        self.assertEqual(snake.limbs[0].rect.x, 160,
                         'New snake leftmost limb should be at 160')

        self.assertEqual(snake.limbs[0].rect.y, 80,
                         'New snake topmost limb should be at 80')

    def test_AppendLimbsExtended(self):
        snake = GameObjectSnake(screen=self.screen,
                                canvas_rect=self.canvas_rect,
                                head_x=48,
                                head_y=16,
                                num_limbs=4,
                                move_direction=MoveDirection.LEFT,
                                block_size=self.block_size)
        self.assertEqual(snake.limbs[0].rect.y, 16)
        self.assertEqual(snake.limbs[0].rect.x, 48)
        self.assertEqual(snake.limbs[1].rect.x, 64)
        self.assertEqual(snake.limbs[2].rect.x, 80)
        self.assertEqual(snake.limbs[3].rect.x, 96)

        snake.move()
        self.assertEqual(snake.limbs[0].rect.x, 32)
        self.assertEqual(snake.limbs[0].rect.y, 16)
        self.assertEqual(snake.limbs[1].rect.x, 48)
        self.assertEqual(snake.limbs[1].rect.y, 16)
        self.assertEqual(snake.limbs[2].rect.x, 64)
        self.assertEqual(snake.limbs[2].rect.y, 16)
        self.assertEqual(snake.limbs[3].rect.x, 80)
        self.assertEqual(snake.limbs[3].rect.y, 16)

        snake.move_down()
        self.assertEqual(snake.limbs[0].rect.x, 32)
        self.assertEqual(snake.limbs[0].rect.y, 32)
        self.assertEqual(snake.limbs[1].rect.x, 32)
        self.assertEqual(snake.limbs[1].rect.y, 16)
        self.assertEqual(snake.limbs[2].rect.x, 48)
        self.assertEqual(snake.limbs[2].rect.y, 16)
        self.assertEqual(snake.limbs[3].rect.x, 64)
        self.assertEqual(snake.limbs[3].rect.y, 16)

        snake.append_limbs(1)
        self.assertEqual(snake.limbs[0].rect.x, 32)
        self.assertEqual(snake.limbs[0].rect.y, 32)
        self.assertEqual(snake.limbs[1].rect.x, 32)
        self.assertEqual(snake.limbs[1].rect.y, 16)
        self.assertEqual(snake.limbs[2].rect.x, 48)
        self.assertEqual(snake.limbs[2].rect.y, 16)
        self.assertEqual(snake.limbs[3].rect.x, 64)
        self.assertEqual(snake.limbs[3].rect.y, 16)

        self.assertEqual(snake.limbs[4].rect.x, 80)
        self.assertEqual(snake.limbs[4].rect.y, 16)

    def test_AppendLimbs(self):
        snake = GameObjectSnake(screen=self.screen,
                        canvas_rect=self.canvas_rect,
                        head_x=48,
                        head_y=16,
                        num_limbs=4,
                        move_direction=MoveDirection.LEFT,
                        block_size=self.block_size)
        self.assertEqual(snake.limbs[0].rect.y, 16)
        self.assertEqual(snake.limbs[0].rect.x, 48)
        self.assertEqual(snake.limbs[1].rect.x, 64)
        self.assertEqual(snake.limbs[2].rect.x, 80)
        self.assertEqual(snake.limbs[3].rect.x, 96)

        snake.append_limbs(3)
        self.assertEqual(snake.limbs[4].rect.x, 112)
        self.assertEqual(snake.limbs[5].rect.x, 0)
        self.assertEqual(snake.limbs[6].rect.x, 16)

        snake = GameObjectSnake(screen=self.screen,
                                canvas_rect=self.canvas_rect,
                                head_x=80,
                                head_y=16,
                                num_limbs=4,
                                move_direction=MoveDirection.RIGHT,
                                block_size=self.block_size)
        self.assertEqual(snake.limbs[0].rect.y, 16)
        self.assertEqual(snake.limbs[0].rect.x, 80)
        self.assertEqual(snake.limbs[1].rect.x, 64)
        self.assertEqual(snake.limbs[2].rect.x, 48)
        self.assertEqual(snake.limbs[3].rect.x, 32)

        snake.append_limbs(3)
        self.assertEqual(snake.limbs[4].rect.x, 16)
        self.assertEqual(snake.limbs[5].rect.x, 0)
        self.assertEqual(snake.limbs[6].rect.x, 112)

        snake = GameObjectSnake(screen=self.screen,
                                canvas_rect=self.canvas_rect,
                                head_x=16,
                                head_y=48,
                                move_direction=MoveDirection.UP,
                                block_size=self.block_size)
        self.assertEqual(snake.limbs[0].rect.x, 16)
        self.assertEqual(snake.limbs[0].rect.y, 48)
        self.assertEqual(snake.limbs[1].rect.y, 64)
        self.assertEqual(snake.limbs[2].rect.y, 80)
        self.assertEqual(snake.limbs[3].rect.y, 96)

        snake.append_limbs(3)
        self.assertEqual(snake.limbs[4].rect.y, 112)
        self.assertEqual(snake.limbs[5].rect.y, 0)
        self.assertEqual(snake.limbs[6].rect.y, 16)

        snake = GameObjectSnake(screen=self.screen,
                                canvas_rect=self.canvas_rect,
                                head_x=16,
                                head_y=80,
                                num_limbs=4,
                                move_direction=MoveDirection.DOWN,
                                block_size=self.block_size)
        self.assertEqual(snake.limbs[0].rect.x, 16)
        self.assertEqual(snake.limbs[0].rect.y, 80)
        self.assertEqual(snake.limbs[1].rect.y, 64)
        self.assertEqual(snake.limbs[2].rect.y, 48)
        self.assertEqual(snake.limbs[3].rect.y, 32)

        snake.append_limbs(3)
        self.assertEqual(snake.limbs[4].rect.y, 16)
        self.assertEqual(snake.limbs[5].rect.y, 0)
        self.assertEqual(snake.limbs[6].rect.y, 112)

    def test_SnakeLimbBlockId(self):
        snake = GameObjectSnake(screen=self.screen,
                                canvas_rect=self.canvas_rect,
                                head_x=32,
                                head_y=16,
                                num_limbs=4,
                                move_direction=MoveDirection.LEFT,
                                block_size=self.block_size)
        self.assertEqual(snake.limbs[0].block_id, 10)
        self.assertEqual(snake.limbs[1].block_id, 11)
        self.assertEqual(snake.limbs[2].block_id, 12)
        self.assertEqual(snake.limbs[3].block_id, 13)

        snake.move()
        self.assertEqual(snake.limbs[0].block_id, 9)
        self.assertEqual(snake.limbs[1].block_id, 10)
        self.assertEqual(snake.limbs[2].block_id, 11)
        self.assertEqual(snake.limbs[3].block_id, 12)

    def test_SnakeCollisionSelf(self):
        snake = GameObjectSnake(screen=self.screen,
                                canvas_rect=self.canvas_rect,
                                head_x=32,
                                head_y=16,
                                num_limbs=5,
                                block_size=self.block_size)
        snake.move_left()
        self.assertFalse(snake.is_collision_self())
        snake.move_down()
        self.assertFalse(snake.is_collision_self())
        snake.move_right()
        self.assertFalse(snake.is_collision_self())
        snake.move_up()
        self.assertTrue(snake.is_collision_self())

    def test_MoveLeft(self):
        snake = GameObjectSnake(screen=self.screen,
                                canvas_rect=self.canvas_rect,
                                head_x=32,
                                head_y=16,
                                num_limbs=4,
                                move_direction=MoveDirection.LEFT,
                                block_size=self.block_size)
        self.assertEqual(snake.limbs[0].rect.y, 16)
        self.assertEqual(snake.limbs[0].rect.x, 32)
        self.assertEqual(snake.limbs[1].rect.x, 48)
        self.assertEqual(snake.limbs[2].rect.x, 64)
        self.assertEqual(snake.limbs[3].rect.x, 80)

        snake.move()
        self.assertEqual(snake.limbs[0].rect.y, 16)
        self.assertEqual(snake.limbs[0].rect.x, 16)
        self.assertEqual(snake.limbs[1].rect.x, 32)
        self.assertEqual(snake.limbs[2].rect.x, 48)
        self.assertEqual(snake.limbs[3].rect.x, 64)

        snake.move()
        self.assertEqual(snake.limbs[0].rect.y, 16)
        self.assertEqual(snake.limbs[0].rect.x, 0)
        self.assertEqual(snake.limbs[1].rect.x, 16)
        self.assertEqual(snake.limbs[2].rect.x, 32)
        self.assertEqual(snake.limbs[3].rect.x, 48)

        # Now first limb snake.limbs[0].rect.x has fallen out on the left and
        # comes back in from the right
        snake.move()
        self.assertEqual(snake.limbs[0].rect.y, 16)
        self.assertEqual(snake.limbs[0].rect.x, 112)
        self.assertEqual(snake.limbs[1].rect.x, 0)
        self.assertEqual(snake.limbs[2].rect.x, 16)
        self.assertEqual(snake.limbs[3].rect.x, 32)

        snake.move()
        self.assertEqual(snake.limbs[0].rect.y, 16)
        self.assertEqual(snake.limbs[0].rect.x, 96)
        self.assertEqual(snake.limbs[1].rect.x, 112)
        self.assertEqual(snake.limbs[2].rect.x, 0)
        self.assertEqual(snake.limbs[3].rect.x, 16)

        snake.move()
        self.assertEqual(snake.limbs[0].rect.y, 16)
        self.assertEqual(snake.limbs[0].rect.x, 80)
        self.assertEqual(snake.limbs[1].rect.x, 96)
        self.assertEqual(snake.limbs[2].rect.x, 112)
        self.assertEqual(snake.limbs[3].rect.x, 0)

        snake.move()
        self.assertEqual(snake.limbs[0].rect.y, 16)
        self.assertEqual(snake.limbs[0].rect.x, 64)
        self.assertEqual(snake.limbs[1].rect.x, 80)
        self.assertEqual(snake.limbs[2].rect.x, 96)
        self.assertEqual(snake.limbs[3].rect.x, 112)

        snake.move()
        self.assertEqual(snake.limbs[0].rect.y, 16)
        self.assertEqual(snake.limbs[0].rect.x, 48)
        self.assertEqual(snake.limbs[1].rect.x, 64)
        self.assertEqual(snake.limbs[2].rect.x, 80)
        self.assertEqual(snake.limbs[3].rect.x, 96)

    def test_MoveRight(self):
        snake = GameObjectSnake(screen=self.screen,
                                canvas_rect=self.canvas_rect,
                                head_x=80,
                                head_y=16,
                                num_limbs=4,
                                move_direction=MoveDirection.RIGHT,
                                block_size=self.block_size)
        self.assertEqual(snake.limbs[0].rect.y, 16)
        self.assertEqual(snake.limbs[0].rect.x, 80)
        self.assertEqual(snake.limbs[1].rect.x, 64)
        self.assertEqual(snake.limbs[2].rect.x, 48)
        self.assertEqual(snake.limbs[3].rect.x, 32)

        snake.move()
        self.assertEqual(snake.limbs[0].rect.y, 16)
        self.assertEqual(snake.limbs[0].rect.x, 96)
        self.assertEqual(snake.limbs[1].rect.x, 80)
        self.assertEqual(snake.limbs[2].rect.x, 64)
        self.assertEqual(snake.limbs[3].rect.x, 48)

        snake.move()
        self.assertEqual(snake.limbs[0].rect.y, 16)
        self.assertEqual(snake.limbs[0].rect.x, 112)
        self.assertEqual(snake.limbs[1].rect.x, 96)
        self.assertEqual(snake.limbs[2].rect.x, 80)
        self.assertEqual(snake.limbs[3].rect.x, 64)

        # Now first limb snake.limbs[0].rect.x has fallen out on the right and
        # comes back in from the left
        snake.move()
        self.assertEqual(snake.limbs[0].rect.y, 16)
        self.assertEqual(snake.limbs[0].rect.x, 0)
        self.assertEqual(snake.limbs[1].rect.x, 112)
        self.assertEqual(snake.limbs[2].rect.x, 96)
        self.assertEqual(snake.limbs[3].rect.x, 80)

        snake.move()
        self.assertEqual(snake.limbs[0].rect.y, 16)
        self.assertEqual(snake.limbs[0].rect.x, 16)
        self.assertEqual(snake.limbs[1].rect.x, 0)
        self.assertEqual(snake.limbs[2].rect.x, 112)
        self.assertEqual(snake.limbs[3].rect.x, 96)

        snake.move()
        self.assertEqual(snake.limbs[0].rect.y, 16)
        self.assertEqual(snake.limbs[0].rect.x, 32)
        self.assertEqual(snake.limbs[1].rect.x, 16)
        self.assertEqual(snake.limbs[2].rect.x, 0)
        self.assertEqual(snake.limbs[3].rect.x, 112)

        snake.move()
        self.assertEqual(snake.limbs[0].rect.y, 16)
        self.assertEqual(snake.limbs[0].rect.x, 48)
        self.assertEqual(snake.limbs[1].rect.x, 32)
        self.assertEqual(snake.limbs[2].rect.x, 16)
        self.assertEqual(snake.limbs[3].rect.x, 0)

        snake.move()
        self.assertEqual(snake.limbs[0].rect.y, 16)
        self.assertEqual(snake.limbs[0].rect.x, 64)
        self.assertEqual(snake.limbs[1].rect.x, 48)
        self.assertEqual(snake.limbs[2].rect.x, 32)
        self.assertEqual(snake.limbs[3].rect.x, 16)

    def test_MoveTop(self):
        snake = GameObjectSnake(screen=self.screen,
                                canvas_rect=self.canvas_rect,
                                head_x=16,
                                head_y=32,
                                num_limbs=4,
                                move_direction=MoveDirection.UP,
                                block_size=self.block_size)
        self.assertEqual(snake.limbs[0].rect.x, 16)
        self.assertEqual(snake.limbs[0].rect.y, 32)
        self.assertEqual(snake.limbs[1].rect.y, 48)
        self.assertEqual(snake.limbs[2].rect.y, 64)
        self.assertEqual(snake.limbs[3].rect.y, 80)

        snake.move()
        self.assertEqual(snake.limbs[0].rect.x, 16)
        self.assertEqual(snake.limbs[0].rect.y, 16)
        self.assertEqual(snake.limbs[1].rect.y, 32)
        self.assertEqual(snake.limbs[2].rect.y, 48)
        self.assertEqual(snake.limbs[3].rect.y, 64)

        snake.move()
        self.assertEqual(snake.limbs[0].rect.x, 16)
        self.assertEqual(snake.limbs[0].rect.y, 0)
        self.assertEqual(snake.limbs[1].rect.y, 16)
        self.assertEqual(snake.limbs[2].rect.y, 32)
        self.assertEqual(snake.limbs[3].rect.y, 48)

        # Now first limb snake.limbs[0].rect.x has fallen out on the top and
        # comes back in from the bottom
        snake.move()
        self.assertEqual(snake.limbs[0].rect.x, 16)
        self.assertEqual(snake.limbs[0].rect.y, 112)
        self.assertEqual(snake.limbs[1].rect.y, 0)
        self.assertEqual(snake.limbs[2].rect.y, 16)
        self.assertEqual(snake.limbs[3].rect.y, 32)

        snake.move()
        self.assertEqual(snake.limbs[0].rect.x, 16)
        self.assertEqual(snake.limbs[0].rect.y, 96)
        self.assertEqual(snake.limbs[1].rect.y, 112)
        self.assertEqual(snake.limbs[2].rect.y, 0)
        self.assertEqual(snake.limbs[3].rect.y, 16)

        snake.move()
        self.assertEqual(snake.limbs[0].rect.x, 16)
        self.assertEqual(snake.limbs[0].rect.y, 80)
        self.assertEqual(snake.limbs[1].rect.y, 96)
        self.assertEqual(snake.limbs[2].rect.y, 112)
        self.assertEqual(snake.limbs[3].rect.y, 0)

        snake.move()
        self.assertEqual(snake.limbs[0].rect.x, 16)
        self.assertEqual(snake.limbs[0].rect.y, 64)
        self.assertEqual(snake.limbs[1].rect.y, 80)
        self.assertEqual(snake.limbs[2].rect.y, 96)
        self.assertEqual(snake.limbs[3].rect.y, 112)

        snake.move()
        self.assertEqual(snake.limbs[0].rect.x, 16)
        self.assertEqual(snake.limbs[0].rect.y, 48)
        self.assertEqual(snake.limbs[1].rect.y, 64)
        self.assertEqual(snake.limbs[2].rect.y, 80)
        self.assertEqual(snake.limbs[3].rect.y, 96)

    def test_MoveDown(self):
        snake = GameObjectSnake(screen=self.screen,
                                canvas_rect=self.canvas_rect,
                                head_x=16,
                                head_y=80,
                                num_limbs=4,
                                move_direction=MoveDirection.DOWN,
                                block_size=self.block_size)
        self.assertEqual(snake.limbs[0].rect.x, 16)
        self.assertEqual(snake.limbs[0].rect.y, 80)
        self.assertEqual(snake.limbs[1].rect.y, 64)
        self.assertEqual(snake.limbs[2].rect.y, 48)
        self.assertEqual(snake.limbs[3].rect.y, 32)

        snake.move()
        self.assertEqual(snake.limbs[0].rect.x, 16)
        self.assertEqual(snake.limbs[0].rect.y, 96)
        self.assertEqual(snake.limbs[1].rect.y, 80)
        self.assertEqual(snake.limbs[2].rect.y, 64)
        self.assertEqual(snake.limbs[3].rect.y, 48)

        snake.move()
        self.assertEqual(snake.limbs[0].rect.x, 16)
        self.assertEqual(snake.limbs[0].rect.y, 112)
        self.assertEqual(snake.limbs[1].rect.y, 96)
        self.assertEqual(snake.limbs[2].rect.y, 80)
        self.assertEqual(snake.limbs[3].rect.y, 64)

        # Now first limb snake.limbs[0].rect.x has fallen out on the bottom and
        # comes back in from the top
        snake.move()
        self.assertEqual(snake.limbs[0].rect.x, 16)
        self.assertEqual(snake.limbs[0].rect.y, 0)
        self.assertEqual(snake.limbs[1].rect.y, 112)
        self.assertEqual(snake.limbs[2].rect.y, 96)
        self.assertEqual(snake.limbs[3].rect.y, 80)

        snake.move()
        self.assertEqual(snake.limbs[0].rect.x, 16)
        self.assertEqual(snake.limbs[0].rect.y, 16)
        self.assertEqual(snake.limbs[1].rect.y, 0)
        self.assertEqual(snake.limbs[2].rect.y, 112)
        self.assertEqual(snake.limbs[3].rect.y, 96)

        snake.move()
        self.assertEqual(snake.limbs[0].rect.x, 16)
        self.assertEqual(snake.limbs[0].rect.y, 32)
        self.assertEqual(snake.limbs[1].rect.y, 16)
        self.assertEqual(snake.limbs[2].rect.y, 0)
        self.assertEqual(snake.limbs[3].rect.y, 112)

        snake.move()
        self.assertEqual(snake.limbs[0].rect.x, 16)
        self.assertEqual(snake.limbs[0].rect.y, 48)
        self.assertEqual(snake.limbs[1].rect.y, 32)
        self.assertEqual(snake.limbs[2].rect.y, 16)
        self.assertEqual(snake.limbs[3].rect.y, 0)

        snake.move()
        self.assertEqual(snake.limbs[0].rect.x, 16)
        self.assertEqual(snake.limbs[0].rect.y, 64)
        self.assertEqual(snake.limbs[1].rect.y, 48)
        self.assertEqual(snake.limbs[2].rect.y, 32)
        self.assertEqual(snake.limbs[3].rect.y, 16)


if __name__ == '__main__':
    unittest.main()
