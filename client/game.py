import pygame
from thread import threaded
from time import sleep as s

# manages game state and user clicks
class Game:

    def __init__(self, board, drawer, client):
        self.board = board
        self.drawer = drawer
        self.client = client

        self.selected_piece = None

        self.drawer.refresh((None, self.board.pieces, None))
    
        self.client.get_opponent_moves()
        self.update_opponent_moves()

    # listen for opponent moves and update the board state
    @threaded
    def update_opponent_moves(self):
        while True:
            move_data = self.client.opponent_moves.get()
            moved_piece = self.board.get_piece_at(move_data["from"])
            moved_piece.attempt_move(move_data["to"])

            if move_data["promo_choice"]:
                moved_piece.promote(move_data["promo_choice"])

            draw_data = (
                None,
                self.board.pieces,
                None,
            )

            self.drawer.refresh(draw_data)

    # show a prompt to the user and handle the promotion of a pawn
    def handle_promotion(self, piece):
        choice_rects = self.drawer.draw_promotion_prompt()
        
        unanswered = True
        choice = ""
        # block until a promotion choice is given
        while unanswered:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()

                if event.type != pygame.MOUSEBUTTONUP:
                    continue

                mouse_pos = pygame.mouse.get_pos()

                for option in choice_rects:
                    if choice_rects[option].collidepoint(mouse_pos):
                        piece.promote(option)
                        choice = option

                        # exit the prompt
                        unanswered = False
        
        return choice
    
    def handle_click(self, mouse_pos: tuple[int, int]):
        if not self.client.turn:
            return
        
        # search for the clicked square
        clicked_square = None
        for square_id, square in self.drawer.squares.items():
            if square.collidepoint(mouse_pos):
                clicked_square = square_id

        if not clicked_square:
            return
    
        clicked_piece = self.board.get_piece_at(clicked_square)
        
        # opponent side piece was clicked with no selected piece
        if clicked_piece is not None and clicked_piece.side != self.drawer.perspective and not self.selected_piece:
            return
        
        # unselect the selected piece if it was clicked again
        if clicked_piece is self.selected_piece:
            self.selected_piece = None
        
        # attempt a move if there is a selected piece
        elif self.selected_piece:
            previous_pos = self.selected_piece.position
            move_status = self.selected_piece.attempt_move(clicked_square)

            promo_data = ""
            if move_status == "promotion":
               promo_data = self.handle_promotion(self.selected_piece)

            if move_status:
                self.client.send_move(move_status, previous_pos, promo_data)

            self.selected_piece = None

        elif clicked_piece:
            self.selected_piece = clicked_piece
        
        draw_data = (
            self.selected_piece.position if self.selected_piece else None,
            self.board.pieces,
            self.selected_piece.get_legal_moves() if self.selected_piece else None,
        )

        # refresh the screen with the draw data
        self.drawer.refresh(draw_data)