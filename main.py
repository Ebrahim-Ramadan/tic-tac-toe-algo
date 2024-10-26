import re
import copy
import sys



EMPTY = " "
XES = "X"
OHS = "O"
MIN_BOARD = 3
MAX_BOARD = 26
NOT_OVER_SCORE = 52 


class TicTacToe:
    # initializes TicTacToe game based on size
    def __init__(self, game_type, size=3, player_xo_choice=XES):
        self.game_type = game_type
        self.size = size
        self.board = []
        for row in range(0,self.size):
            new_row = []
            for col in range(0,self.size):
                new_row.append(EMPTY)
            self.board.append(new_row)
        self.winner = EMPTY
        self.num_moves = 0  # keeps track of whether there is a draw
        self.max_moves = self.size * self.size
        self.player = XES  # whose turn it is
        self.prev_move = ()
        self.quit = False

        # the following variables are only used when playing against the computer:
        # computer is OHS or XES (whatever person didn't pick)
        if player_xo_choice == XES:
            self.computer = OHS
        else:
            self.computer = XES
        self.score = NOT_OVER_SCORE
        self.board_possibilities = {}

    # copy constructor
    def copy_game(self):
        return copy.deepcopy(self)

    #find out if playing in 2 player mode or against computer
    @staticmethod
    def get_game_type():
        while True:
            game_type = raw_input("Enter 1 to play against computer or 2 to play in two player mode: ")
            if game_type == "1" or game_type == "2":
                return int(game_type)
            else:
                print( "You must select 1 or 2.")