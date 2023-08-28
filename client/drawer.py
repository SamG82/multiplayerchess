import pygame
import images
pygame.init()

from typing import Literal

# drawer for menus and prompts
class MenuDrawer:

    # styles
    font_size = 32
    font = pygame.font.Font("freesansbold.ttf", font_size)

    def __init__(self, screen):
        self.screen = screen

    # draws a popup with given text, size, and position to the screen
    def message_popup(self, text: str, width: int, height: int, position: tuple[int, int]=None):
        if position is None:
            position = self.screen.get_rect().center

        # container for extra padding
        container = pygame.Rect(0, 0, width, height)
        container.center = position

        message = MenuDrawer.font.render(text, True, "black", "white")
        rect = message.get_rect()
        rect.center = position

        pygame.draw.rect(self.screen, "white", container)
        self.screen.blit(message, rect)
        

# drawer for the game-related components
class BoardDrawer:

    # styles
    size_scale = 0.93
    piece_scale = 0.78
    move_marker_scale = 0.38
    promotion_prompt_color = (128,) * 3

    square_files = 'abcdefgh'
    square_ranks = [i for i in range(1, 9)]

    square_starts = {
        "w": (-7, 0),
        "b": (0, -7)
    }

    def __init__(self, screen, perspective: Literal["w", "b"]):
        self.perspective = perspective
        self.screen = screen

        center = self.screen.get_rect().center
        size = BoardDrawer.size_scale * self.screen.get_height()
        
        # rect for the entire board
        self.rect = pygame.Rect((0, 0), (size,) * 2)
        self.rect.center = center

        # square size and range of points to draw squares at
        self.square_size = int(self.rect.width / 8)
        self.square_columns = range(self.rect.left, self.rect.right, self.square_size)
        self.square_rows = range(self.rect.top, self.rect.bottom, self.square_size)

        self.piece_size = BoardDrawer.piece_scale * self.square_size
        self.move_marker_size = BoardDrawer.move_marker_scale * self.square_size

        # draw the rectangle for the entire board
        pygame.draw.rect(self.screen, "black", self.rect, 1)

        self.squares: dict[str, pygame.Rect] = dict()
        self.pieces: dict[str, pygame.Rect] = dict()

        rank_start, file_start = BoardDrawer.square_starts[self.perspective]
        self.rank_start = rank_start
        self.file_start = file_start

        self.selected_square = None
        self.piece_locations = dict()

    # draws the board
    def draw(self):
        start_light = True

        # draw the grid
        for rank, y in enumerate(self.square_rows, start=self.rank_start):
            for file, x in enumerate(self.square_columns, start=self.file_start):
                square_name = f"{BoardDrawer.square_files[abs(file)]}{BoardDrawer.square_ranks[abs(rank)]}"
                square_rect = None

                if self.selected_square and square_name == self.selected_square:
                    square_rect = self.screen.blit(images.get("yellow_square", self.square_size), (x, y))

                elif start_light:
                    square_rect = self.screen.blit(images.get("light_square", self.square_size), (x, y))

                else:
                    square_rect = self.screen.blit(images.get("dark_square", self.square_size), (x, y))
                
                self.squares[square_name] = square_rect
                start_light = not start_light

                piece_name = self.piece_locations.get(square_name, None)
                if not piece_name:
                    continue
                
                piece_img, piece_rect = images.get(piece_name, self.piece_size, need_rect=True)

                # center the piece with the square
                piece_rect.center = square_rect.center
                self.screen.blit(piece_img, piece_rect)
                self.pieces[square_name] = piece_rect

            start_light = not start_light

    # draw the promotion prompt, returns a list of rects that house the promotion options
    def draw_promotion_prompt(self):
        container = pygame.Rect(0, 0, self.square_size * 4, self.square_size)
        container.center = self.rect.center

        choice_rects = dict()
        options = ['q', 'r', 'b', 'n']

        x_values = list(range(container.left, container.right, self.square_size))

        # draw rects across the container
        for option, x in zip(options, x_values):
            choice_rect = pygame.Rect(x, container.y, self.square_size, self.square_size)

            image_name = f"{self.perspective}{option}"
            image = images.get(image_name, self.piece_size)
            
            image_rect = image.get_rect()
            image_rect.center = choice_rect.center

            choice_rects[option] = choice_rect

            pygame.draw.rect(self.screen, BoardDrawer.promotion_prompt_color, choice_rect)
            self.screen.blit(image, image_rect)
        
        # for black border
        pygame.draw.rect(self.screen, "black", container, 4)
        pygame.display.flip()

        return choice_rects