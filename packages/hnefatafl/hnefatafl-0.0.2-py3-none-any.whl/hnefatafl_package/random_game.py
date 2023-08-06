from tafl_board import TaflBoard
from random import sample

tafl = TaflBoard()  # Create the board object
tafl.render_console()   # Render the board in the console

while not tafl.check_game_over():
    valid_moves = tafl.get_all_valid_moves()
    move = sample(valid_moves,1)[0] # returns a list of length 1.
    tafl.make_move(move)
    tafl.render_console()
