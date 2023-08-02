import copy

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
    sq1_x, sq1_y = get_square_coordinates(square1)
    sq2_x, sq2_y = get_square_coordinates(square2)
    
    return abs(sq1_x - sq2_x) + abs(sq1_y - sq2_y)


class Board:

    def __init__(self):
        self.pieces = []
        backrank_order = [Rook, Knight, Bishop, Queen,
                        King, Bishop, Knight, Rook]
        
        for i in range(1, 9):
            b_backrank = backrank_order[i-1]("black", i, self)
            w_backrank = backrank_order[i-1]("white", i+56, self)
            
            b_pawn = Pawn("black", i+8, self)
            w_pawn = Pawn("white", i+48, self)

            self.pieces.extend([b_backrank, w_backrank, b_pawn, w_pawn])

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
    
    #return a list of pieces on a given side
    def get_side_pieces(self, side: str):
        return [piece for piece in self.pieces if piece.side == side]

    # removes a piece at a given position from the board
    def remove_piece_at(self, position: int):
        self.pieces = [piece for piece in self.pieces if piece.position != position]

    # returns true or false if the given side is in check
    def in_check(self, side: str) -> bool:
        [king] = [piece for piece in self.get_side_pieces(side) if piece.name == f"king_{side}"]
        return king.is_attacked()
    
    # returns a side's name if it is checkmated
    def is_checkmate(self):
        for side in ["white", "black"]:
            pieces = self.get_side_pieces(side)
            legal_moves = []

            for piece in pieces:
                legal_moves.extend(piece.get_legal_moves())

            if len(legal_moves) == 0:
                return side
        
        return None

class Piece:

    def __init__(self, side: str, initial_position: int, board: Board):
        self.position: int = initial_position
        self.side: str = side
        self.board: Board = board
        self.name: str = f"{type(self).__name__}_{self.side}".lower()
        self.opposite_side = "black" if self.side == "white" else "white"

    # gets a list of moves given the current board state, doesn't take check into account
    def pseudo_legal_moves(self) -> list[int]:
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
    
    # makes sure a move wouldn't violate rules of check
    def move_is_legal(self, move):
        # create a temporary board and piece copy
        temp_board = copy.deepcopy(self.board)
        temp_piece = temp_board.get_piece_at(self.position)

        # remove the piece from the temporary board if its a capture
        if temp_piece.is_capture(move):
            temp_board.remove_piece_at(move)

        # move the copied piece
        temp_piece.position = move

        # if the copied board is still in check, then the move isn't valid
        if temp_board.in_check(self.side):
            return False
        
        return True
    
    # get all legal moves that could be played
    def get_legal_moves(self):
        return [move for move in self.pseudo_legal_moves() if self.move_is_legal(move)]
    
    # returns true or false if a move is a capture of an enemy piece or not
    def is_capture(self, move: int) -> bool:        
        opposing_positions = self.board.side_positions(self.opposite_side)

        return move in opposing_positions

    # update the piece position to the move if it's valid, handles capturing
    def attempt_move(self, move: int) -> bool:
        if move not in self.get_legal_moves():
            return False

        if self.is_capture(move):
            self.board.remove_piece_at(move)

        self.position = move

        return True

    # returns true or false if piece is attacked by another
    def is_attacked(self) -> bool:
        opposing_moves = []

        for piece in self.board.get_side_pieces(self.opposite_side):
            opposing_moves.extend(piece.pseudo_legal_moves())

        return self.position in opposing_moves
    
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
    
    # list of pseudo legal knight moves
    def pseudo_legal_moves(self) -> list[int]:
        moves = []
        
        same_side_positions = self.board.side_positions(self.side)

        for offset in Knight.offsets:
            move = self.position + offset
            if self.valid_knight_move(move) and move not in same_side_positions:
                moves.append(move)

        return moves

class Pawn(Piece):
    
    # conditional attack offsets for pawn depending on color
    attack_offsets = {
        "white": (-9, -7),
        "black": (9, 7)
    }

    # conditional movement offsets for non-attacking moves
    movement_offsets = {
        "white": -8,
        "black": 8
    }

    def __init__(self, side: str, initial_position: int, board: Board):
        super().__init__(side, initial_position, board)
        self.has_moved = False
    
    def attempt_move(self, move: int) -> bool:
        # reduce the pawn's range if it has moved
        if super().attempt_move(move):
            self.has_moved = True

    # pseudo legal moves for pawn
    def pseudo_legal_moves(self) -> list[int]:
        moves = []

        # add the diagonal moves if they are attacks
        for offset in Pawn.attack_offsets[self.side]:
            potential_move = self.position + offset
            if self.is_capture(potential_move) and get_distance(self.position, potential_move) == 2:
                moves.append(potential_move)

        # pawns can either move by 8 or 16 if they haven't moved
        shortrange_move = self.position + Pawn.movement_offsets[self.side]
        longrange_move = self.position + Pawn.movement_offsets[self.side] * 2

        # add the shortrange move if it isnt blocked
        if self.board.get_piece_at(shortrange_move):
            return moves
        
        moves.append(shortrange_move)

        # add the long range move if the pawn is on its starting position and isnt blocked
        if not self.has_moved and not self.board.get_piece_at(longrange_move):
            moves.append(longrange_move)

        return moves