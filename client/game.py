import pygame
import images
from chess import Board

class Game:

    def __init__(self, screen):
        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        self.rect = None
        
        self.squares = dict()
        self.board = Board()

    # sets up the board dimensions and draws the initial grid
    def draw_grid(self):
        center = self.screen_rect.center
        size = 0.93 * self.screen_rect.height 
        
        # rect for the entire board
        self.rect = pygame.Rect((0, 0), (size,) * 2)
        self.rect.center = center

        square_size = int(self.rect.width / 8)

        # scale images to the correct square size
        dark_square = pygame.transform.scale(images.dark_square, (square_size,) * 2)
        light_square = pygame.transform.scale(images.light_square, (square_size,) * 2)
        
        # draw the rectangle for the entire board
        pygame.draw.rect(self.screen, "black", self.rect, 1)

        square_id = 1

        # boolean to flip when alternating light and dark squares
        start_light = True

        x_values = range(self.rect.left, self.rect.right, square_size)
        y_values = range(self.rect.top, self.rect.bottom, square_size)

        # draw the grid
        for y in y_values:
            for x in x_values:
                
                square_rect = None
                # alternate light and dark squares
                if start_light:
                    square_rect = self.screen.blit(light_square, (x, y))
                else:
                    square_rect = self.screen.blit(dark_square, (x, y))

                self.squares[square_id] = square_rect
                
                square_id += 1

                start_light = not start_light

            start_light = not start_light
