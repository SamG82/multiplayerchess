
class Game:
    def __init__(self, board, drawer):
        self.board = board
        self.drawer = drawer
        self.selected_piece = None

        self.drawer.refresh((None, self.board.pieces, None))

    # able to move both sides just for testing
    def handle_click_test(self, mouse_pos: tuple[int, int]):
        
        clicked_square = None
        for square_id, square in self.drawer.squares.items():
            if square.collidepoint(mouse_pos):
                clicked_square = square_id

        clicked_piece = self.board.get_piece_at(clicked_square)
        if clicked_piece is self.selected_piece:
            self.selected_piece = None
        
        elif self.selected_piece and (clicked_piece is None or clicked_piece.side != self.selected_piece.side):
            self.selected_piece.attempt_move(clicked_square)
            self.selected_piece = None

        elif clicked_piece:
            self.selected_piece = clicked_piece
        
        draw_data = (
            self.selected_piece.position if self.selected_piece else None,
            self.board.pieces,
            self.selected_piece.get_legal_moves() if self.selected_piece else None
        )
        self.drawer.refresh(draw_data)