import pygame
from game_object_snake import MoveDirection
from game import Game

# Set the display dimension
VP_WIDTH = 640
VP_HEIGHT = 480
size = [VP_WIDTH, VP_HEIGHT]

pygame.init()
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

game = Game(screen, block_size=32)
game.render()

done = False
speed_counter = 0
collision_counter = 0
game.set_speed(10)
events = pygame.event.get()
while not done:
    for event in events:
        match event.type:
            case pygame.constants.QUIT:
                done = True
            case pygame.constants.KEYDOWN:
                match event.key:
                    case pygame.constants.K_ESCAPE:
                        done = True
                    case pygame.constants.K_RIGHT:
                        game.append_new_direction(MoveDirection.RIGHT)
                    case pygame.constants.K_LEFT:
                        game.append_new_direction(MoveDirection.LEFT)
                    case pygame.constants.K_UP:
                        game.append_new_direction(MoveDirection.UP)
                    case pygame.constants.K_DOWN:
                        game.append_new_direction(MoveDirection.DOWN)
                    case pygame.constants.K_1:
                        game.set_speed(5)
                    case pygame.constants.K_2:
                        game.set_speed(10)
                    case pygame.constants.K_3:
                        game.set_speed(20)
                    case pygame.constants.K_4:
                        game.set_speed(30)
                    case pygame.constants.K_5:
                        game.set_speed(60)

    if speed_counter < 60:
        speed_counter += game.get_speed()
    else:
        speed_counter = 0
        game.update()
        game.render()

    pygame.display.flip()
    clock.tick(60)
    events = pygame.event.get()
