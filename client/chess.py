top_row = list(range(1, 9))
bottom_row = list(range(57, 65))
left_column = list(range(1, 58, 8))
right_column = list(range(8, 65, 8))

# maps each type of linear moving direction to what borders it could possibly hit
border_map: dict[int, list] = {
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
def get_square_coordinates(square: int) -> tuple[int, int]:
    row = int(square/8.01) + 1
    column = None

    for possible_column in range(1, 9):
        if (possible_column - square) % 8 == 0:
            column = possible_column

    return (row, column)

# gets the horizontal and vertical distance between two squares
def get_distance(square1: int, square2: int) -> int:
    move_x, move_y = get_square_coordinates(square1)
    position_x, position_y = get_square_coordinates(square2)

    return abs(move_x - position_x) + abs(move_y - position_y)


class Board:

    def __init__(self):
        self.pieces = []
        starting_order = [Rook, Knight, Bishop, Queen,
                        King, Bishop, Knight, Rook]
        
        for i in range(0, 8):
            b_piece = starting_order[i]("black", i + 1, self)
            w_piece = starting_order[i]("white", i + 57, self)

            self.pieces.append(b_piece)
            self.pieces.append(w_piece)

class Piece:

    def __init__(self, side: str, initial_position: int, board: Board):
        self.position: int = initial_position
        self.side: str = side
        self.board: Board = board
        self.image_name: str = f"{type(self).__name__}_{self.side}".lower()


    # gets a list of valid moves given the current board state for linearly moving pieces
    def get_moves(self) -> list[int]:
        piece_positions = [piece.position for piece in self.board.pieces if piece.position != self.position]
        
        # get the other piece positions from the board
        same_side_positions = []
        for piece in self.board.pieces:
            if piece.side == self.side and piece.position != self.position:
                same_side_positions.append(piece.position)

        all_moves = []

        # rotate through each direction
        for offset in self.offsets:
            new_move = self.position
            squares_traveled = 0
            
            # make sure the move hasn't reached a border or another piece's position
            while new_move not in border_map[offset] and new_move not in piece_positions:
                squares_traveled += 1
                if squares_traveled > self.reach:
                    break
                
                # traverse each direction by incrementing by the offset amount
                new_move += offset

                # add the move if it isn't blocked by a same-side piece
                if new_move not in same_side_positions:
                    all_moves.append(new_move)

        return all_moves
    
    # update the piece position to the move if it's valid
    def make_move(self, move: int) -> bool:
        if move in self.get_moves():
            self.position = move
            return True
        
        return False


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
    
    # knight moves can be validated by how far away they are
    def valid_knight_move(self, move: int) -> bool:
        within_bounds = move > 0 and move < 65
        within_range = get_distance(self.position, move) < 4

        return within_range and within_bounds
    
    def get_moves(self) -> list[int]:
        moves = []
        
        same_side_positions = [piece.position for piece in self.board.pieces if piece.side == self.side]
        for offset in Knight.offsets:
            move = self.position + offset

            if self.valid_knight_move(move) and move not in same_side_positions:
                moves.append(move)

        return moves

