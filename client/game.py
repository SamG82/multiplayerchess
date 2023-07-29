import pygame
import images
from chess import Board

class Game:
    size_scale = 0.93
    piece_scale = 0.78
    move_marker_scale = 0.38
    
    def __init__(self, screen, perspective: str):
        self.board = Board()
        self.perspective = perspective
        self.screen = screen

        center = self.screen.get_rect().center
        size = Game.size_scale * self.screen.get_height()
        
        # rect for the entire board
        self.rect = pygame.Rect((0, 0), (size,) * 2)
        self.rect.center = center

        # square size and range of points to draw squares at
        self.square_size = int(self.rect.width / 8)
        self.square_columns = range(self.rect.left, self.rect.right, self.square_size)
        self.square_rows = range(self.rect.top, self.rect.bottom, self.square_size)

        self.piece_size = Game.piece_scale * self.square_size
        self.move_marker_size = Game.move_marker_scale * self.square_size

        # draw the rectangle for the entire board
        pygame.draw.rect(self.screen, "black", self.rect, 1)

        # state variables for interaction
        self.squares: dict[int, pygame.Rect] = dict()
        self.selected_piece = None

    # draws squares for the grid
    def draw_squares(self):
        square_id = 1

        # boolean to flip when alternating light and dark squares
        start_light = True

        # draw the grid
        for y in self.square_rows:
            for x in self.square_columns:
                square_rect = None

                if self.selected_piece is not None and square_id == self.selected_piece.position:
                    square_rect = self.screen.blit(images.get("yellow_square", self.square_size), (x, y))

                elif start_light:
                    square_rect = self.screen.blit(images.get("light_square", self.square_size), (x, y))

                else:
                    square_rect = self.screen.blit(images.get("dark_square", self.square_size), (x, y))

                self.squares[square_id] = square_rect
                square_id += 1

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
    def draw_pieces(self):
        for piece in self.board.pieces:
            self.draw_centered_image(piece.image_name, piece.position, self.piece_size)

    # draw any move markers if there are any
    def draw_markers(self):
        if self.selected_piece is None: return
        
        for square in self.selected_piece.get_moves():
            self.draw_centered_image("move_marker", square, self.move_marker_size, 100)

    # handle each click from the player
    def handle_click(self, mouse_pos: tuple[int, int]):

        # get the clicked square
        clicked_square = None
        for square_id, square in self.squares.items():
            if square.collidepoint(mouse_pos):
                clicked_square = square_id

        # look up if there is a clicked piece by square
        clicked_piece = self.board.get_piece_at(clicked_square)
        
        # click is already the selected piece, unselect it
        if clicked_piece is self.selected_piece:
            self.selected_piece = None
            return
        
        # clicked a same-side piece
        if clicked_piece and clicked_piece.side == self.perspective:
            self.selected_piece = clicked_piece
            return
        
        # clicked an enemy piece or square while a piece is a selected, attempt move
        if self.selected_piece and (clicked_piece is None or clicked_piece.side != self.perspective):
            self.selected_piece.attempt_move(clicked_square)
            self.selected_piece = None