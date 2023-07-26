import pygame
import images
from chess import Board


class Game:
    size_scale = 0.93
    piece_scale = 0.78
    move_highlight_scale = 0.38
    
    def __init__(self, screen):
        self.board = Board()
        self.screen = screen

        center = self.screen.get_rect().center
        size = Game.size_scale * self.screen.get_height()
        
        # rect for the entire board
        self.rect = pygame.Rect((0, 0), (size,) * 2)
        self.rect.center = center

        self.square_size = int(self.rect.width / 8)
        self.square_columns = range(self.rect.left, self.rect.right, self.square_size)
        self.square_rows = range(self.rect.top, self.rect.bottom, self.square_size)

        # scale images to the correct square size
        self.dark_square = pygame.transform.scale(images.dark_square, (self.square_size,) * 2)
        self.light_square = pygame.transform.scale(images.light_square, (self.square_size,) * 2)
        self.yellow_square = pygame.transform.scale(images.yellow_square, (self.square_size,) * 2)
        
        self.move_highlight = pygame.transform.scale(images.move_marker, (self.move_highlight_scale * self.square_size,) * 2)
        self.move_highlight.set_alpha(100)

        # draw the rectangle for the entire board
        pygame.draw.rect(self.screen, "black", self.rect, 1)

        # state variables for interaction
        self.squares = dict()
        self.selected_piece = None
        self.potential_move_squares = []


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
                    square_rect = self.screen.blit(self.yellow_square, (x, y))

                elif start_light:
                    square_rect = self.screen.blit(self.light_square, (x, y))

                else:
                    square_rect = self.screen.blit(self.dark_square, (x, y))

                self.squares[square_id] = square_rect
                square_id += 1

                start_light = not start_light

            start_light = not start_light
        
    def draw_pieces(self):
        for piece in self.board.pieces:
            piece_image = images.piece_images[str(piece)]
            scaled_image = pygame.transform.scale(piece_image, (Game.piece_scale * self.square_size,) * 2)
            
            piece_rect = scaled_image.get_rect()
            piece_rect.center = self.squares[piece.position].center

            self.screen.blit(scaled_image, piece_rect)

    def draw_markers(self):
        for square in self.potential_move_squares:
            
            highlight_rect = self.move_highlight.get_rect()
            highlight_rect.center = square.center
            
            self.screen.blit(self.move_highlight, highlight_rect)

    def handle_click(self, mouse_pos):

        # get the clicked square
        clicked_square = None
        for square_id, square in self.squares.items():
            if square.collidepoint(mouse_pos):
                clicked_square = square_id

        # look up if there is a clicked piece by square
        clicked_piece = None
        for piece in self.board.pieces:
            if piece.position == clicked_square:
                clicked_piece = piece

        # unselect the selected piece if it was clicked again
        if clicked_piece == self.selected_piece:
            self.selected_piece = None

        elif clicked_piece is not None:
            self.selected_piece = clicked_piece

        # no selected piece, clear the potential moves
        if self.selected_piece is None:
            self.potential_move_squares = []
            return
        
        self.potential_move_squares = [self.squares[move] for move in self.selected_piece.get_moves()]

        # make the move, clear selected piece and moves
        if clicked_square in self.selected_piece.get_moves():
            self.selected_piece.make_move(clicked_square)
            self.selected_piece = None
            self.potential_move_squares = []
