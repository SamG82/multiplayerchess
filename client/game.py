import pygame

# manages game state and user clicks
class Game:

    def __init__(self, board, drawer, client):
        self.board = board
        self.drawer = drawer
        self.client = client

        self.selected_piece = None
        self.drawer.refresh((None, self.board.pieces, None))

    # show a prompt to the user and handle the promotion of a pawn
    def handle_promotion(self, piece):
        choice_rects = self.drawer.draw_promotion_prompt()
        
        unanswered = True
        
        # block until a promotion choice is given
        while unanswered:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()

                if event.type == pygame.MOUSEBUTTONUP:
                    mouse_pos = pygame.mouse.get_pos()

                    for option in choice_rects:
                        if choice_rects[option].collidepoint(mouse_pos):
                            piece.promote(option)

                            # exit the prompt
                            unanswered = False
    
    def handle_click(self, mouse_pos: tuple[int, int]):
        
        # search for the clicked square
        clicked_square = None
        for square_id, square in self.drawer.squares.items():
            if square.collidepoint(mouse_pos):
                clicked_square = square_id

        clicked_piece = self.board.get_piece_at(clicked_square)
        
        # opponent side piece was clicked
        if clicked_piece is not None and clicked_piece.side != self.drawer.perspective:
            return
        
        # unselect the selected piece if it was clicked again
        if clicked_piece is self.selected_piece:
            self.selected_piece = None
        
        # attempt a move if there is a selected piece
        elif self.selected_piece:
            move_status = self.selected_piece.attempt_move(clicked_square)

            if move_status == "promotion":
               self.handle_promotion(self.selected_piece)

            if move_status:
                self.client.send_move(clicked_square)
                
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