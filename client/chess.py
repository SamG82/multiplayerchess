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

    # a list of all piece positions except for a piece at an excluded position
    def all_positions(self, exclude_position=0):
        return [piece.position for piece in self.pieces if piece.position != exclude_position]
    
    # a list of all piece positions for a particular side except for a piece at an excluded position
    def side_positions(self, side: str, exclude_position=0):
        return [piece.position for piece in self.pieces if piece.side == side and piece.position != exclude_position]
    
    # return the specific piece at a given position
    def get_piece_at(self, position: int):
        correct_piece = None

        for piece in self.pieces:
            if piece.position == position:
                correct_piece = piece

        return correct_piece
    
    # removes a piece at a given position from the board
    def remove_piece_at(self, position: int):
        self.pieces = [piece for piece in self.pieces if piece.position != position]


class Piece:

    def __init__(self, side: str, initial_position: int, board: Board):
        self.position: int = initial_position
        self.side: str = side
        self.board: Board = board
        self.image_name: str = f"{type(self).__name__}_{self.side}".lower()
        self.opposite_side = "black" if self.side == "white" else "white"

    # gets a list of valid moves given the current board state for linearly moving pieces
    def get_moves(self) -> list[int]:
        all_moves = []

        # rotate through each direction
        for offset in self.offsets:
            new_move = self.position
            squares_traveled = 0
            
            # make sure the move hasn't reached a border or another piece's position
            while new_move not in border_map[offset] and new_move not in self.board.all_positions(self.position):
                squares_traveled += 1
                if squares_traveled > self.reach:
                    break
                
                # traverse each direction by incrementing by the offset amount
                new_move += offset

                # add the move if it isn't blocked by a same-side piece
                if new_move not in self.board.side_positions(self.side, self.position):
                    all_moves.append(new_move)

        return all_moves
    
    # returns true or false if a move is a capture of an enemy piece or not
    def is_capture(self, move: int) -> bool:        
        opposing_positions = self.board.side_positions(self.opposite_side)

        return move in opposing_positions

    # remove the pieces from the board if it's captured
    def handle_capture(self, move):
        if not self.is_capture(move):
            return
        
        self.board.remove_piece_at(move)


    # update the piece position to the move if it's valid
    def attempt_move(self, move: int):
        if move not in self.get_moves():
            return

        self.handle_capture(move)
        self.position = move
        

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

