import pygame
import images

class Board:

    def __init__(self, screen):
        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        self.rect = None

    # sets up the board dimensions and draws the initial grid
    def draw(self):
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

        # boolean to flip when alternating light and dark squares
        start_light = True

        # draw the grid
        for row in range(self.rect.left, self.rect.right, square_size):
            for column in range(self.rect.top, self.rect.bottom, square_size):

                square_rect = None
    
                # alternate light and dark squares
                if start_light:
                    square_rect = self.screen.blit(light_square, (row, column))
                else:
                    square_rect = self.screen.blit(dark_square, (row, column))

                start_light = not start_light
            start_light = not start_light