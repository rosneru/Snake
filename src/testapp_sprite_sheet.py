import pygame
import os
import sys
from sprite_sheet import SpriteSheet


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode([640, 480])
    clock = pygame.time.Clock()

    sheet_image = os.path.join('../gfx', 'snake-graphics.png')
    sheet = SpriteSheet(sheet_image, 4, 5)

    max_index = sheet.get_num_frames() - 1
    index = 0
    counter = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    sys.exit()
        screen.blit(sheet.get_frame(index), (0, 0))
        pygame.display.flip()
        clock.tick(60)

        counter += 1
        if counter > 60:
            counter = 0
            index += 1
            if index > max_index:
                index = 0
