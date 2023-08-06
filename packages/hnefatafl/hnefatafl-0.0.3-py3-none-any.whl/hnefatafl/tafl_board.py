#===============================================================================
# Tafl Gym Environment
#
# Description: Implements a generic tafl board class and provides functions to
#              display and manipulate the game for use in an OpenAI Gym
#              environment.
#===============================================================================

# Numpy arrays
import numpy as np

# System stdout
import sys

#===============================================================================
#                               CLASS DEFINITION
#===============================================================================
class TaflBoard():

    def __init__(self):

        # 0 = empty square
        # 1 = black soldier square
        # 2 = white soldier square
        # 3 = king square
        # 4 = escape square
        board = np.array([[4, 0, 0, 1, 1, 1, 1, 1, 0, 0, 4],
                          [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [1, 0, 0, 0, 0, 2, 0, 0, 0, 0, 1],
                          [1, 0, 0, 0, 2, 2, 2, 0, 0, 0, 1],
                          [1, 1, 0, 2, 2, 3, 2, 2, 0, 1, 1],
                          [1, 0, 0, 0, 2, 2, 2, 0, 0, 0, 1],
                          [1, 0, 0, 0, 0, 2, 0, 0, 0, 0, 1],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                          [4, 0, 0, 1, 1, 1, 1, 1, 0, 0, 4]])
        self.board = board

        # Populate the pieces matrix with a piece based on the square type
        # 0 = empty
        # 1 = black soldier
        # 2 = white soldier
        # 3 = white king
        pieces = np.copy(self.board)
        pieces[pieces == 4] = 0
        self.pieces = pieces

        # Black always starts
        self.turn = -1
        self.game_over = False

    #---------------------------------------------------------------------------
    # Name:        make_move
    # Description: Makes a move
    # Arguments:   - move: dict with 'from' and 'to' entries
    # Returns:	   1 if the defenders win, -1 if attackers win, 0 otherwise
    #---------------------------------------------------------------------------
    def make_move(self, move):
        return self.move_piece(move['from'], move['to'])

    #---------------------------------------------------------------------------
    # Name:        move_piece
    # Description: Moves a piece to a new square
    # Arguments:   - piece_pos: position of the piece to be moved
    #              - new_pos: position to move the piece to
    # Returns:	   1 if the defenders win, -1 if attackers win, 0 otherwise
    #---------------------------------------------------------------------------
    def move_piece(self, piece_pos, new_pos):
        xi = piece_pos[0]
        yi = piece_pos[1]
        xf = new_pos[0]
        yf = new_pos[1]

        # Check that there is a piece in piece_pos and no piece in new_pos
        if not self.piece_at(piece_pos) or self.piece_at(new_pos):
            return None

        # Check that the piece belongs to the play whose turn it is
        if not self.team(self.piece_at(piece_pos)) == self.turn:
            return None

        # Check that the move is valid
        valid_moves = self.get_valid_moves(piece_pos)
        if not any(x['to'] == new_pos for x in valid_moves):
            return None

        # Move the piece to the new position
        self.pieces[new_pos] = self.piece_at(piece_pos)
        self.pieces[piece_pos[0],piece_pos[1]] = 0

        # Get captures
        captures = self.get_captures(new_pos)

        # Remove captured pieces
        for capture in captures:
            self.pieces[capture[0],capture[1]] = 0

        self.turn = -1 if self.turn == 1 else 1
        return self.check_game_over()

    #---------------------------------------------------------------------------
    # Name:        check_game_over
    # Description: Checks if the game is in a terminal state
    # Returns:	   1 if the defenders win, -1 if attackers win, 0 otherwise
    #---------------------------------------------------------------------------
    def check_game_over(self):
        pieces = self.pieces
        rows = len(pieces)
        cols = len(pieces[0])
        king_square = []

        # Find the king
        for i in range(rows):
            for j in range(cols):
                if pieces[i,j] == 3:
                    king_square = [i,j]
                    break

        # Check if the king is on an escape square
        if self.square_at(king_square) == 4:
            return 1

        #Check of the king has been captured
        directions = [[-1,0], [+1,0], [0,-1], [0,+1]]
        surrounded = []
        surrounded += [self.team(self.piece_at(king_square, dir)) == self.team(1) or
                       self.square_at(king_square, dir) == 3 for dir in directions]
        if all(surrounded):
            return -1

        #TODO: Check for repeated states (draw)

        #TODO: No valid moves available constitutes a loss

        # Return 0 if the game is not over
        return 0


    #---------------------------------------------------------------------------
    # Name:        piece_to_char
    # Description: Returns a character representing the given piece type for
    #              display on the console.
    # Arguments:   - piece: piece type
    # Returns:     Character representing the piece.
    #---------------------------------------------------------------------------
    def piece_to_char(self, piece):
        if piece == 0:
        	return " "
        elif piece == 1:
            return "●"
        elif piece == 2:
            return "o"
        elif piece == 3:
            return "ø"
        else:
            return None

    #---------------------------------------------------------------------------
    # Name:        render_console
    # Description: Renders the board in text on the console.
    #---------------------------------------------------------------------------
    def render_console(self):

        pieces = self.pieces
        rows = len(pieces)
        cols = len(pieces[0])
        outfile = sys.stdout

        # Write the top edge of the board
        outfile.write('  ')
        outfile.write('-' * (2*cols+1))
        outfile.write('\n')

        # Loop over every cell on the board
        for i in range(cols):

            # Write the row number and a line on the left edge of the board.
            outfile.write('{:2}|'.format(i))

            for j in range(rows):

                piece = pieces[i,j]
                char = self.piece_to_char(pieces[i,j])
                if j == cols-1:
                    outfile.write('{}'.format(char))
                else:
                    outfile.write('{} '.format(char))

            # Write a line on the right side of the board
            outfile.write('|\n')

        # Write the bottom edge of the board with colum number
        outfile.write('  ')
        outfile.write('-' * (2*cols+1))
        outfile.write('\n  ')
        for i in range(cols):
            outfile.write(' {}'.format(i))
        outfile.write('\n'*2)

    #---------------------------------------------------------------------------
    # Name:        render_moves_console
    # Description: Renders the board in text on the console with valid moves
    #              highlighted for the given piece.
    #---------------------------------------------------------------------------
    def render_moves_console(self, square):

        pieces = self.pieces
        rows = len(pieces)
        cols = len(pieces[0])
        outfile = sys.stdout
        valid_moves = self.get_valid_moves(square)

        # Write the top edge of the board
        outfile.write('  ')
        outfile.write('-' * (2*cols+1))
        outfile.write('\n')

        # Loop over every cell on the board
        for i in range(cols):

            # Write the row number and a line on the left edge of the board.
            outfile.write('{:2}|'.format(i))

            for j in range(rows):

                # If the square is in the list of valid moves, write the
                # character showing a valid move. Otherwise, write the piece
                # character
                if any(x['to'] == (i,j) for x in valid_moves):

                    # Do not put a space after the last piece in the row
                    if j == cols-1:
                        outfile.write('∙')
                    else:
                        outfile.write('∙ ')

                else:

                    # Do not put a space after the last piece in the row
                    char = self.piece_to_char(pieces[i,j])
                    if j == cols-1:
                        outfile.write('{}'.format(char))
                    else:
                        outfile.write('{} '.format(char))

            # Write a line on the right side of the board
            outfile.write('|\n')

        # Write the bottom edge of the board with colum number
        outfile.write('  ')
        outfile.write('-' * (2*cols+1))
        outfile.write('\n  ')
        for i in range(cols):
            outfile.write(' {}'.format(i))
        outfile.write('\n'*2)

    #---------------------------------------------------------------------------
    # Name:        render_window
    # Description: Renders the board graphically in a window.
    #---------------------------------------------------------------------------
    def render_window():
        pass

    #---------------------------------------------------------------------------
    # Name:        get_all_valid_moves
    # Description: Gets a list of all valid moves for the player whose turn it
    #              is. The list of moves is a list of dicts containing the
    #              start and end coordinates for the move.
    # Returns:     List of valid moves for the player whose turn it is.
    #---------------------------------------------------------------------------
    def get_all_valid_moves(self):

        valid_moves = []

        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if self.team(self.piece_at([i,j])) == self.turn:
                    valid_moves += self.get_valid_moves([i,j])

        return valid_moves

    #---------------------------------------------------------------------------
    # Name:        get_valid_moves
    # Description: Gets a list of all valid moves for a piece at the given
    #              square. The list of moves is a list of dicts containing the
    #              start and end coordinates for the move.
    # Arguments:   - square: square coordinates
    # Returns:     List of valid moves for the piece at the given square.
    #---------------------------------------------------------------------------
    def get_valid_moves(self, square):

        # All pieces move like rooks in Chess. Add coordinates in the up, down,
        # left, and right directions until reaching another piece or the end of
        # the board. Additionally, pieces that are not the king may not stop on
        # the king's square or the escape squares

        valid_moves = []
        rows = len(self.board)
        cols = len(self.board[0])
        start_x = square[0]
        start_y = square[1]

        # We must check in every direction (up, down, left, and right) for valid
        # squares to move to. Loop in each direction adding the moves to the
        # list of valid moves until the edge of the board or another piece is
        # reached
        for dir in [[-1,0], [+1,0], [0,-1], [0,+1]]:
            next_square = self.offset(square, dir)
            while next_square != None:
                if self.piece_at(next_square):
                    break
                else:
                    valid_moves += [{'from': square, 'to': next_square}]
                    next_square = self.offset(next_square, dir)

        # If the piece being moved is not the king, remove all king squares and
        # escape squares from the list of valid moves
        if self.piece_at(square) != 3:
            valid_moves = [x for x in valid_moves if
                self.square_at(x['to']) != 3 and
                self.square_at(x['to']) != 4]

        return valid_moves

    #---------------------------------------------------------------------------
    # Name:        offset
    # Description: Gets the coordinates of a square with an offset from the
    #              given square. For example, the coordinates of the square
    #              above square [3,2] can be found using offset([3,2],[-1,0]).
    #              Returns None if there is no square at that offset since it is
    #              off of the board.
    # Arguments:   - square: square coordinates
    #              - offset: square offset
    # Returns:     Coordinates of the square at the given offset from the given
    #              square. None if the offset square if off of the board.
    #---------------------------------------------------------------------------
    def offset(self, square, offset=[0,0]):
        rows = len(self.board)
        cols = len(self.board[0])
        x = square[0] + offset[0]
        y = square[1] + offset[1]
        return (x,y) if 0 <= x < rows and 0 <= y < cols else None

    #---------------------------------------------------------------------------
    # Name:        square_at
    # Description: Gets the square type at the given square with the given
    #              offset. Returns None if there is no square at that offset
    #              since it is off of the board.
    # Arguments:   - square: square coordinates
    #              - offset: square offset
    # Returns:     Type of the square at the given offset from the given
    #              square. None if the offset square if off of the board.
    #---------------------------------------------------------------------------
    def square_at(self, square, offset=[0,0]):
        coords = self.offset(square, offset)
        return self.board[coords] if coords != None else None

    #---------------------------------------------------------------------------
    # Name:        square_at
    # Description: Gets the piece type at the given square with the given
    #              offset. Returns None if there is no square at that offset
    #              since it is off of the board.
    # Arguments:   - square: square coordinates
    #              - offset: square offset
    # Returns:     Type of the piece at the given offset from the given
    #              square. None if the offset square if off of the board.
    #---------------------------------------------------------------------------
    def piece_at(self, square, offset=[0,0]):
        coords = self.offset(square, offset)
        return self.pieces[coords] if coords != None else None

    #---------------------------------------------------------------------------
    # Name:        team
    # Description: Gets the team that the piece type belongs to.
    # Arguments:   - piece: piece type
    # Returns:     Team of a piece of the given type.
    #---------------------------------------------------------------------------
    def team(self, piece):
        if piece == 1:
            return -1
        elif piece == 2 or piece == 3:
            return 1
        else:
            return None

    #---------------------------------------------------------------------------
    # Name:        get_captures
    # Description: Gets a list of captures caused by a piece at the given
    #              square. This assumes that the piece has just moved to the
    #              specified square.
    # Arguments:   - square: square coordinates
    # Returns:     List of captures caused by a piece at the given square.
    #---------------------------------------------------------------------------
    def get_captures(self, square):

        # A piece is captured if it becomes sandwiched between two enemy pieces
        # by an enemy's move. The king's spawning square and the escape squares
        # also count as an enemy for the purpose of capturing. However, a white
        # is not captured by being sandwiched between a black piece and the
        # king's square if the king is still on the square.

        captures = []

        # If there is not a piece at the square, there is no point checking for
        # captures. The king also cannot be captured by normal means.
        if self.piece_at(square):
            piece = self.piece_at(square)

            # We must check in every direction for captures (up, down, left, and
            # right)
            directions = [[-1,0], [+1,0], [0,-1], [0,+1]]
            for dir in directions:

                # Get the pieces and squares that are offset from the piece in
                # the given direction
                piece_dir = self.piece_at(square, dir)
                piece_two_dir = self.piece_at(square, [i*2 for i in dir])
                square_two_dir = self.square_at(square, [i*2 for i in dir])

                # If the piece in this direction is an ally of the piece, there
                # is clearly no capture in that direction. If the piece in this
                # direction is the king, it cannot be captured by normal means
                if self.team(piece_dir) != self.team(piece) and piece_dir != 3:

                    # Check the three capture methods
                    capture_by_piece = self.team(piece_two_dir) == self.team(piece)
                    capture_by_king_square = square_two_dir == 3 and piece_two_dir != 3
                    capture_by_escape_square = square_two_dir == 4

                    # If any capture method applies, add it to the list of captures
                    if (capture_by_piece or
                        capture_by_king_square or
                        capture_by_escape_square):
                        captures += [self.offset(square, dir)]

        return captures


    #---------------------------------------------------------------------------
    # Name:        get_state
    # Description: Returns the board as a vector
    # Returns:     vector representing all piece locations on the board
    #---------------------------------------------------------------------------
    def get_state(self):
        return self.pieces.reshape((1,11*11))

    #---------------------------------------------------------------------------
    # Name:        get_similar_states
    # Description: Returns all states that can be transformed into the
    #              current state via rotations and reflections of the board.
    # Returns:     Matrix representing all piece locations on the board
    #              including the current state. Rows are states.
    #---------------------------------------------------------------------------
    def get_similar_states(self):
        state1 = self.pieces.reshape((1,11*11))
        state1r = np.flip(self.pieces,0).reshape((1,11*11))
        state2 = np.rot90(self.pieces,1).reshape((1,11*11))
        state2r = np.flip(np.rot90(self.pieces,1)).reshape((1,11*11))
        state3 = np.rot90(self.pieces,2).reshape((1,11*11))
        state3r = np.flip(np.rot90(self.pieces,2)).reshape((1,11*11))
        state4 = np.rot90(self.pieces,3).reshape((1,11*11))
        state4r = np.flip(np.rot90(self.pieces,3)).reshape((1,11*11))
        return np.array([state1, state1r, state2, state2r, state3, state3r, state4, state4r])

    #---------------------------------------------------------------------------
    # Name:        get_similar_states
    # Description: Returns all states that can be transformed into the
    #              input state via rotations and reflections of the board.
    # Returns:     Matrix representing all piece locations on the board
    #              including the input state. Rows are states.
    #---------------------------------------------------------------------------
    def get_similar_states(self, n_state):
        state = n_state.reshape(11,11)
        state1 = n_state
        state1r = np.flip(state,0).reshape((1,11*11))
        state2 = np.rot90(state,1).reshape((1,11*11))
        state2r = np.flip(np.rot90(state,1)).reshape((1,11*11))
        state3 = np.rot90(state,2).reshape((1,11*11))
        state3r = np.flip(np.rot90(state,2)).reshape((1,11*11))
        state4 = np.rot90(state,3).reshape((1,11*11))
        state4r = np.flip(np.rot90(state,3)).reshape((1,11*11))
        return np.array([state1, state1r, state2, state2r, state3, state3r, state4, state4r])
