import pygame
import images

FONT_SIZE = 32
FONT = pygame.font.Font("freesansbold.ttf", FONT_SIZE)

# drawer for menus and prompts
class MenuDrawer:
    
    def __init__(self, screen):
        self.screen = screen

    # draws a popup with given text, size, and position to the screen
    def message_popup(self, text: str, width: int, height: int, position: tuple[int, int]=None):
        if position is None:
            position = self.screen.get_rect().center

        message = FONT.render(text, True, "black", "white")
        rect = message.get_rect()

        rect.center = position
        rect.width = width
        rect.height = height

        self.screen.blit(message, rect)
        pygame.display.flip()


# drawer for the game-related components
class ChessDrawer:

    # styles
    size_scale = 0.93
    piece_scale = 0.78
    move_marker_scale = 0.38
    promotion_prompt_color = (128,) * 3

    def __init__(self, screen, perspective: str):
        self.perspective = perspective
        self.screen = screen

        center = self.screen.get_rect().center
        size = ChessDrawer.size_scale * self.screen.get_height()
        
        # rect for the entire board
        self.rect = pygame.Rect((0, 0), (size,) * 2)
        self.rect.center = center

        # square size and range of points to draw squares at
        self.square_size = int(self.rect.width / 8)
        self.square_columns = range(self.rect.left, self.rect.right, self.square_size)
        self.square_rows = range(self.rect.top, self.rect.bottom, self.square_size)

        self.piece_size = ChessDrawer.piece_scale * self.square_size
        self.move_marker_size = ChessDrawer.move_marker_scale * self.square_size

        # draw the rectangle for the entire board
        pygame.draw.rect(self.screen, "black", self.rect, 1)

        self.squares: dict[int, pygame.Rect] = dict()

    # draws squares for the grid
    def draw_squares(self, selected_square):

        # start from 64 to "reverse" the perspective of the board for black
        square_id = 1 if self.perspective == "white" else 64

        # boolean to flip when alternating light and dark squares
        start_light = True

        # draw the grid
        for y in self.square_rows:
            for x in self.square_columns:
                square_rect = None

                if selected_square is not None and square_id == selected_square:
                    square_rect = self.screen.blit(images.get("yellow_square", self.square_size), (x, y))

                elif start_light:
                    square_rect = self.screen.blit(images.get("light_square", self.square_size), (x, y))

                else:
                    square_rect = self.screen.blit(images.get("dark_square", self.square_size), (x, y))

                self.squares[square_id] = square_rect

                # count down if black is the perspective
                square_id += 1 if self.perspective == "white" else -1

                # flip boolean to draw the opposite square
                start_light = not start_light

            start_light = not start_light
    
    # generic drawing function for images centered to a specific square
    def draw_centered_image(self, image_name: str, square_id: int, size: int, alpha: int = 255):
        image = images.get(image_name, size, alpha)
        rect = image.get_rect()
        rect.center = self.squares[square_id].center
        self.screen.blit(image, rect)

    # draw the pieces to the board
    def draw_pieces(self, pieces):
        for piece in pieces:
            self.draw_centered_image(piece.name, piece.position, self.piece_size)

    # draw any move markers
    def draw_markers(self, moves):
        if moves is None: return
        
        for square in moves:
            self.draw_centered_image("move_marker", square, self.move_marker_size, 100)

    # draw the promotion prompt, returns a list of rects that house the promotion options
    def draw_promotion_prompt(self):
        container = pygame.Rect(0, 0, self.square_size * 4, self.square_size)
        container.center = self.rect.center

        choice_rects = dict()
        options = ["Queen", "Bishop", "Rook", "Knight"]

        x_values = list(range(container.left, container.right, self.square_size))

        # draw rects across the container
        for option, x in zip(options, x_values):
            choice_rect = pygame.Rect(x, container.y, self.square_size, self.square_size)

            image_name = f"{option.lower()}_{self.perspective}"
            image = images.get(image_name, self.piece_size)
            
            image_rect = image.get_rect()
            image_rect.center = choice_rect.center

            choice_rects[option] = choice_rect

            pygame.draw.rect(self.screen, ChessDrawer.promotion_prompt_color, choice_rect)
            self.screen.blit(image, image_rect)
        
        # for black border
        pygame.draw.rect(self.screen, "black", container, 4)
        pygame.display.flip()

        return choice_rects

    def get_squares(self):
        return self.squares

    def refresh(self, draw_data: tuple):
        selected, pieces, moves = draw_data

        self.draw_squares(selected)
        self.draw_pieces(pieces)
        self.draw_markers(moves)