top_row = list(range(1, 9))
bottom_row = list(range(57, 65))
left_column = list(range(1, 58, 8))
right_column = list(range(8, 65, 8))

# maps each type of linear moving direction to what borders it could possibly hit
border_map = {
    -1: left_column,
    1: right_column,
    -7: top_row + right_column,
    7: bottom_row + left_column,
    -8: top_row,
    8: bottom_row,
    -9: top_row + left_column,
    9: bottom_row + right_column,
}

# gets the cartesian coordinates of the square position from int
def get_square_coordinates(square):
    row = int(square/8.01) + 1
    column = None

    for possible_column in range(1, 9):
        if (possible_column - square) % 8 == 0:
            column = possible_column

    return (row, column)

# gets the horizontal and vertical distance between two squares
def get_distance(square1, square2):
    move_x, move_y = get_square_coordinates(square1)
    position_x, position_y = get_square_coordinates(square2)

    return abs(move_x - position_x) + abs(move_y - position_y)


class Piece:

    def __init__(self, side, initial_position):
        self.position = initial_position
        self.side = side
    
    # gets a list of valid moves given the current board state for linearly moving pieces
    def get_moves(self, game_board):
        piece_positions = [piece.position for piece in game_board.pieces if piece.position != self.position]
        
        same_side_positions = []
        for piece in game_board.pieces:
            if piece.side == self.side and piece.position != self.position:
                same_side_positions.append(piece.position)

        all_moves = []
        new_move = self.position

        for offset in self.offsets:
            squares_traveled = 0
            while new_move not in border_map[offset] and new_move not in piece_positions:
                squares_traveled += 1
                if squares_traveled > self.reach:
                    break
                
                new_move += offset

                if new_move not in same_side_positions:
                    all_moves.append(new_move)

            new_move = self.position

        return all_moves
    
    def __str__(self):
        return f"{type(self).__name__}_{self.side}".lower()

class Rook(Piece):
    
    # horizontal, vertical
    offsets = (-1, 1, -8, 8)
    reach = 7


class Bishop(Piece):

    # diagonals
    offsets = (-7, 7, -9, 9)
    reach = 7


class Queen(Piece):

    # can just combine the Rook and Bishop offsets
    offsets = Rook.offsets + Bishop.offsets
    reach = 7


class King(Piece):
    
    # moves the same way as queen
    offsets = Queen.offsets
    reach = 1


class Knight(Piece):

    offsets = (-17, -15, -10, -6, 6, 10, 15, 17)
    
    def valid_knight_move(self, move):
        within_bounds = move > 0 and move < 65
        within_range = get_distance(self.position, move) < 4

        return within_range and within_bounds
    
    def get_moves(self, game_board):
        moves = []
        
        same_side_positions = [piece.position for piece in game_board.pieces if piece.side == self.side]
        for offset in Knight.offsets:
            move = self.position + offset

            if self.valid_knight_move(move) and move not in same_side_positions:
                moves.append(move)

        return moves

class Board:

    starting_order = [Rook, Knight, Bishop, Queen,
                      King, Bishop, Knight, Rook]
    
    def __init__(self):
        self.pieces = []

        for i in range(1, 9):
            b_piece = Board.starting_order[i-1]("black", i)
            w_piece = Board.starting_order[i-1]("white", i + 56)

            self.pieces.append(b_piece)
            self.pieces.append(w_piece)
