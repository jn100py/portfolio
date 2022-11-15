"""
As chess.py is currently being refactored, we use a mocked version of this file,
to demo our Flask chess application.

The Flask file models.py imports Game defined below.

The following moves result in a response from the computer
e2 e4 -> d7 d5
d2 d3 -> f7 f5

The next move restarts the game.
"""

import os
import sys

MYPARENTPATH = '/'.join(os.path.realpath(__file__).split('/')[0:-2])

sys.path.append(MYPARENTPATH + '/chess_app/shared')
from files import read_stelling_data


def load_cb_stelling(stelling_nr):

    filepath = f'{MYPARENTPATH}/chess_app/data/mock_stellingen/stelling_{stelling_nr}.txt'

    return read_stelling_data(filepath)


class Piece:
    def __init__(self, name):
        self.name = name
        self.on_board = True


class Game:
    def __init__(self,  name, startsituation_file, do_simulation=True,
                 do_not_print_all_info=False, my_color=False,
                 current_color_to_play = 'white', current_color_not_to_play = 'black'):

        self.name = name

        self.startsituation_file = startsituation_file
        self.do_simulation = do_simulation
        self.do_not_print_all_info = do_not_print_all_info

        self.my_color = my_color
        self.current_color_to_play = current_color_to_play
        self.current_color_not_to_play = current_color_not_to_play

        self.pieces = [Piece('a')]
        self.message = ""

        self.startsituation = self.__import_startsituation_data()

    def __import_startsituation_data(self):

        with open(self.startsituation_file, 'r') as file:
            data = file.read()

        return data

    def calculate_possible_moves(self):
        return

    def check_check(self, piece_name, current_color_not_to_play=False):
        return False

    def move_pieces(self, move_nr, move, ai_level, simulation, show_board):
        return True

    def show_board_simple(self, number):

        if self.startsituation == load_cb_stelling(2):
            return load_cb_stelling(3).split('\n')

        if self.startsituation == load_cb_stelling(4):
            return load_cb_stelling(5).split('\n')

        if self.startsituation == load_cb_stelling(101): # used by test: test_c_move_white_queen
            return load_cb_stelling(102).split('\n')

        return load_cb_stelling(1).split('\n')

    @property
    def current_possible_moves(self):

        if self.startsituation == load_cb_stelling(2):
            return {17: ['Pawn', ['a3', 'a4'], 'a2'], 18: ['Pawn', ['b3', 'b4'], 'b2'], 
                    19: ['Pawn', ['c3', 'c4'], 'c2'], 20: ['Pawn', ['d3', 'd4'], 'd2'], 
                    21: ['Pawn', ['f3', 'f4'], 'f2'], 22: ['Pawn', ['g3', 'g4'], 'g2'],
                    23: ['Pawn', ['h3', 'h4'], 'h2'], 24: ['Pawn', ['f5', 'd5', 'e5'], 'e4'],
                    26: ['Knight', ['a3', 'c3'], 'b1'], 27: ['Bishop', [], 'c1'], 
                    28: ['Queen', ['e2', 'f3', 'g4', 'h5'], 'd1'],
                    29: ['King', ['e2'], 'e1'], 30: ['Bishop', ['e2', 'd3', 'c4', 'b5', 'a6'], 'f1'], 
                    31: ['Knight', ['f3', 'h3', 'e2'], 'g1']}

        if self.startsituation == load_cb_stelling(4):
            return {17: ['Pawn', ['a3', 'a4'], 'a2'], 18: ['Pawn', ['b3', 'b4'], 'b2'], 
                    19: ['Pawn', ['c3', 'c4'], 'c2'], 20: ['Pawn', ['d4'], 'd3'], 
                    21: ['Pawn', ['f3', 'f4'], 'f2'], 22: ['Pawn', ['g3', 'g4'], 'g2'],
                    23: ['Pawn', ['h3', 'h4'], 'h2'], 24: ['Pawn', ['f5', 'd5', 'e5'], 'e4'],
                    26: ['Knight', ['a3', 'c3', 'd2'], 'b1'], 
                    27: ['Bishop', ['d2', 'e3', 'f4', 'g5', 'h6'], 'c1'],
                    28: ['Queen', ['e2', 'f3', 'g4', 'h5', 'd2'], 'd1'], 
                    29: ['King', ['e2', 'd2'], 'e1'],
                    30: ['Bishop', ['e2'], 'f1'], 31: ['Knight', ['f3', 'h3', 'e2'], 'g1']}

        if self.startsituation == load_cb_stelling(100): # used by test: test_c_move_white_queen
            return {17: ['Queen', ['a8', 'a7', 'a6', 'a5', 'a4', 'a3'], 'a2']}

        if self.startsituation == load_cb_stelling(101):
            return {}

        return {17: ['Pawn', ['a3', 'a4'], 'a2'], 18: ['Pawn', ['b3', 'b4'], 'b2'], 
                19: ['Pawn', ['c3', 'c4'], 'c2'], 20: ['Pawn', ['d3', 'd4'], 'd2'], 
                21: ['Pawn', ['e4', 'e3'], 'e2'], 22: ['Pawn', ['f3', 'f4'], 'f2'],
                23: ['Pawn', ['g3', 'g4'], 'g2'], 24: ['Pawn', ['h3', 'h4'], 'h2'],
                26: ['Knight', ['a3', 'c3'], 'b1'], 31: ['Knight', ['f3', 'h3'], 'g1']}
