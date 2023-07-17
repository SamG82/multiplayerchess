class Piece:
    all_positions = list(range(1, 65))

    def __init__(self, initial_position):
        self.position = initial_position

class Rook(Piece):
    def get_moves(self):
        horizontal_moves = []
        vertical_moves = []

        rightmost_move = 0
        if self.position % 8 == 0:
            rightmost_move = self.position
        else:
            rightmost_move = self.position+(8-self.position % 8)
        
        horizontal_moves = Piece.all_positions[rightmost_move-8:rightmost_move]
        vertical_moves = [i for i in Piece.all_positions if (self.position-i) % 8 == 0]
        
        return list(filter(lambda x: x != self.position, (horizontal_moves + vertical_moves)))

