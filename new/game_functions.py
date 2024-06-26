import numpy as np


POSSIBLE_MOVES_COUNT = 4
CELL_COUNT = 4
NUMBER_OF_SQUARES = CELL_COUNT * CELL_COUNT
NEW_TILE_DISTRIBUTION = np.array([2, 2, 2, 2, 2, 2, 2, 2, 2, 4]) #9 2's and 1 4's since in 2048, 90% --> 2 and 10% --> 1#


def initialize_game():
    board = np.zeros((NUMBER_OF_SQUARES), dtype="int")
    initial_twos = np.random.default_rng().choice(NUMBER_OF_SQUARES, 2, replace=False) #it is returned as a numpy array
    board[initial_twos] = 2
    board = board.reshape((CELL_COUNT, CELL_COUNT))
    return board


def check_for_win(board):
    return 2048 in board


