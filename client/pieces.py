from board import Board

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
    
    # gets custom barriers for pieces that have shorter range
    def get_limited_barrier_range(self, direction_offsets):
        barriers = Piece.directions_edges

        for offset in direction_offsets:
            try:
                # add the new barrier
                barriers[offset].append(self.position + offset)
            except KeyError:
                # barrier doesn't exist. make a list for it
                barriers[offset] = [self.position + offset]

        return barriers

    # gets a list of moves in each direction up until the barriers
    def generate_linear_moves(self, direction_offsets, barriers=None):
        if barriers is None:
            barriers = Piece.directions_edges

        all_moves = []
            
        new_move = self.position

        # traverse each possible direction from the starting position
        for direction in direction_offsets:

            # move and append the possible new_move in the corresponding direction until it reaches an edge
            while new_move not in barriers[direction]:
                new_move += direction
                all_moves.append(new_move)

            # reset for the next direction
            new_move = self.position

        return all_moves
       

class Rook(Piece):
    
    # horizontal, vertical
    offsets = (-1, 1, -8, 8)

    def get_moves(self):
        return self.generate_linear_moves(Rook.offsets)
        

class Bishop(Piece):

    # diagonals
    offsets = (-7, 7, -9, 9)

    def get_moves(self):
        return self.generate_linear_moves(Bishop.offsets)
    

class Queen(Piece):

    # can just combine the Rook and Bishop offsets
    offsets = Rook.offsets + Bishop.offsets

    def get_moves(self):
        return self.generate_linear_moves(Queen.offsets)


class King(Piece):
        
    def get_moves(self):
        
        # use the same queen offsets
        return self.generate_linear_moves(Queen.offsets, self.get_limited_barrier_range(Queen.offsets))


class Knight(Piece):

    offsets = (-17, -15, -10, -6, 6, 10, 15, 17)

    def get_moves(self):
        
        # filters out knight moves that are too far away from the current position
        def validate_move(move):
            if move < 1 or move > 64:
                return False
            
            move_x, move_y = Board.get_square_coordinates(move)
            position_x, position_y = Board.get_square_coordinates(self.position)

            # move is too far away to be valid
            if abs(position_x - move_x) + abs(position_y-move_y) > 4:
                return False
            
            return True
            
        unfiltered_moves = self.generate_linear_moves(Knight.offsets, self.get_limited_barrier_range(Knight.offsets))

        # filter out the moves that aren't possible
        filtered_moves = list(filter(validate_move, unfiltered_moves))

        return filtered_moves