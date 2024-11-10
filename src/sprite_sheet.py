from typing import List
import os
import pygame


class SpriteSheet:

    def __init__(self, filename: str, num_rows: int, num_columns: int):
        if not os.path.isfile(filename):
            # No file at give path. So assuming the given file path as being
            # relative to this python file and trying again.
            absolute_path = os.path.dirname(__file__)
            relative_path = filename
            filename = os.path.join(absolute_path, relative_path)

        if not os.path.isfile(filename):
            print(f"No file found at path: {filename}")
            raise SystemExit()

        try:
            self.sheet = pygame.image.load(filename).convert_alpha()
        except pygame.error as e:
            print(f"Unable to load sprite sheet image: {filename}")
            raise SystemExit(e)

        self.frame_width = self.sheet.get_width() / num_columns
        self.frame_height = self.sheet.get_height() / num_rows
        self.num_frames = num_columns * num_rows

        self.frames: List[pygame.surface.Surface] = []

        empty_surface = pygame.Surface(
            (self.frame_width, self.frame_height)).convert_alpha()
        frame_size = [self.frame_width, self.frame_height]
        for row in range(0, num_rows):
            for column in range(0, num_columns):
                frame = pygame.Surface(frame_size, pygame.SRCALPHA)
                x_start = column * self.frame_width
                y_start = row * self.frame_height
                area_rect = pygame.Rect(
                    x_start, y_start, self.frame_width, self.frame_height)
                frame.blit(self.sheet, dest=(0, 0), area=area_rect)

                # TODO need to skip empty surfaces
                if frame != empty_surface:
                    self.frames.append(frame)

    def get_sheet(self) -> pygame.surface.Surface:
        return self.sheet

    def get_frames(self) -> List[pygame.surface.Surface]:
        return self.frames

    def get_frame(self, index: int) -> pygame.surface.Surface:
        return self.frames[index]

    def get_num_frames(self) -> int:
        return len(self.frames)
