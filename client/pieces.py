
class Piece:
    
    # board representation:
    """
    1  2  3  4  5  6  7  8
    9  10 11 12 13 14 15 16
    17 18 19 20 21 22 23 24
    25 26 27 28 29 30 31 32
    33 34 35 36 37 38 39 40
    41 42 43 44 45 46 47 48
    49 50 51 52 53 54 55 56
    57 58 59 60 61 62 63 64
    """

    top_row = list(range(1, 9))
    left_column = list(range(1, 58, 8))
    bottom_row = list(range(57, 65))
    right_column = list(range(8, 65, 8))

    # maps each possible linear movement direction to the edges it could collide with
    directions_edges = {
        -1: left_column,
        1: right_column,
        -7: top_row + right_column,
        7: bottom_row + left_column,
        -8: top_row,
        8: bottom_row,
        -9: top_row + left_column,
        9: bottom_row + right_column
    }
    
    def __init__(self, initial_position):
        self.position = initial_position

    def generate_linear_moves(self, *direction_offsets):
        all_moves = []
            
        new_move = self.position

        # traverse each possible direction from the starting position
        for direction in direction_offsets:

            # move and append the possible new_move in the corresponding direction until it reaches an edge
            while new_move not in Piece.directions_edges[direction]:
                new_move += direction
                all_moves.append(new_move)

            # reset for the next direction
            new_move = self.position

        return all_moves
       

class Rook(Piece):
    
    # horizontal, vertical
    offsets = (-1, 1, -8, 8)

    def get_moves(self):
        return self.generate_linear_moves(*Rook.offsets)
        

class Bishop(Piece):

    # diagonals
    offsets = (-7, 7, -9, 9)

    def get_moves(self):
        return self.generate_linear_moves(*Bishop.offsets)
    
class Queen(Piece):

    # can just combine the Rook and Bishop offsets
    def get_moves(self):
        return self.generate_linear_moves(*(Rook.offsets + Bishop.offsets))
