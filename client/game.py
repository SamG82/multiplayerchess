import pygame
import images
from chess import Board

class Game:
    size_scale = 0.93
    piece_scale = 0.78
    move_highlight_scale = 0.38
    
    def __init__(self, screen):
        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        center = self.screen_rect.center
        size = Game.size_scale * self.screen_rect.height 
        
        # rect for the entire board
        self.rect = pygame.Rect((0, 0), (size,) * 2)
        self.rect.center = center

        self.square_size = int(self.rect.width / 8)

        # scale images to the correct square size
        self.dark_square = pygame.transform.scale(images.dark_square, (self.square_size,) * 2)
        self.light_square = pygame.transform.scale(images.light_square, (self.square_size,) * 2)

        self.move_highlight = pygame.transform.scale(images.move_marker, (self.move_highlight_scale * self.square_size,) * 2)
        self.move_highlight.set_alpha(100)

        # draw the rectangle for the entire board
        pygame.draw.rect(self.screen, "black", self.rect, 1)

        self.squares = dict()
        self.board = Board()
        self.selected_square = None
        self.current_moves = []


    # draws squares for the grid
    def draw_squares(self):
        square_id = 1

        # boolean to flip when alternating light and dark squares
        start_light = True

        x_values = range(self.rect.left, self.rect.right, self.square_size)
        y_values = range(self.rect.top, self.rect.bottom, self.square_size)

        # draw the grid
        for y in y_values:
            for x in x_values:
                
                square_rect = None

                # alternate light and dark squares
                if start_light:
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
        for square in self.current_moves:
            
            highlight_rect = self.move_highlight.get_rect()
            highlight_rect.center = square.center
            
            self.screen.blit(self.move_highlight, highlight_rect)

    def handle_piece_click(self, mouse_pos):
        clicked_square = None
        for square_id, square in self.squares.items():
            if square.collidepoint(mouse_pos):
                clicked_square = square_id

        clicked_piece = None
        for piece in self.board.pieces:
            if piece.position == clicked_square:
                clicked_piece = piece

        if clicked_piece == None:
            return
        
        potential_moves = clicked_piece.get_moves(self.board)
        self.current_moves = [self.squares[move] for move in potential_moves]