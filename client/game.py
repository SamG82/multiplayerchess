import pygame

class Game:
    def __init__(self, board, drawer):
        self.board = board
        self.drawer = drawer
        self.selected_piece = None

        self.drawer.refresh((None, self.board.pieces, None))

    # show a prompt to the user and handle the promotion of a pawn
    def handle_promotion(self, piece):
        choice_rects = self.drawer.draw_promotion_prompt()
        
        unanswered = True
        
        # block until a promotion choice is given
        while unanswered:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    mouse_pos = pygame.mouse.get_pos()

                    for option in choice_rects:
                        if choice_rects[option].collidepoint(mouse_pos):
                            piece.promote(option)

                            # exit the prompt
                            unanswered = False

    # able to move both sides just for testing
    def handle_click_test(self, mouse_pos: tuple[int, int]):
        
        clicked_square = None
        for square_id, square in self.drawer.squares.items():
            if square.collidepoint(mouse_pos):
                clicked_square = square_id

        clicked_piece = self.board.get_piece_at(clicked_square)

        # unselect the selected piece if it was clicked again
        if clicked_piece is self.selected_piece:
            self.selected_piece = None
        
        # attempt a move if there is a selected piece and possible move square was clicked
        elif self.selected_piece and (clicked_piece is None or clicked_piece.side != self.selected_piece.side):
            move_status = self.selected_piece.attempt_move(clicked_square)
            
            # handle possible promotion of a pawn
            if move_status == "promotion":
               self.handle_promotion(self.selected_piece)

            # unselect the piece after a move has been attempted
            self.selected_piece = None

        elif clicked_piece:
            self.selected_piece = clicked_piece
        
        draw_data = (
            self.selected_piece.position if self.selected_piece else None,
            self.board.pieces,
            self.selected_piece.get_legal_moves() if self.selected_piece else None,
        )

        # refresh the screen
        self.drawer.refresh(draw_data)