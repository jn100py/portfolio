import sys
import os
import datetime
from itertools import groupby
from flask_sqlalchemy import SQLAlchemy

from chess_app.shared.files import read_stelling_data
from chess_app.config_.constants import CONVERSION_TABLE_HOR, CONVERSION_TABLE_VERT,\
                                        CONVERT2LPOS, CONVERT2TPOS,\
                                        REL_PATH_CURRENT_GAME_FILE

MYPATH = '/'.join(os.path.realpath(__file__).split('/')[0:-1])
MYPARENTPATH = '/'.join(os.path.realpath(__file__).split('/')[0:-2])
FILEPATH_CURRENT_GAME = MYPATH + REL_PATH_CURRENT_GAME_FILE

sys.path.append(MYPARENTPATH + '/chess_app_basic')

MOCK = True
if MOCK:
    from chess_mock import Game as TerminalGame
else:
    from chess import Game as TerminalGame


db = SQLAlchemy()


def cleanup_cb_stelling(stelling_chessboard):
    """When white has captured a piece, the black piece needs to
    be removed from the board.
    This was not yet solved client side.
    """

    stelling_lines = stelling_chessboard.split('\n')
    squares_with_pieces = []
    for line in stelling_lines:
        square, _, _ = line.split(' ')
        squares_with_pieces.append(square)


    square_used_twice = False
    for key, group in groupby(sorted(squares_with_pieces), lambda square: square):
        if len(list(group)) > 1:
            square_used_twice = key
            break

    if square_used_twice:

        color_computer = 'black'

        def check_is_square_with_a_valid_piece(line):
            if line.startswith(square_used_twice) and color_computer in line:
                return False
            return True

        stelling_lines = list(filter(check_is_square_with_a_valid_piece, stelling_lines))

    return "\n".join(stelling_lines)


def convert_html2cb_stelling(stelling_html):
    """Example (1 piece): img_piece_rook_black_1,564,128
    converted to: a8 black Rook\n
    """

    def convert(pos_left, pos_top):
        return f"{CONVERSION_TABLE_HOR[pos_left]}{CONVERSION_TABLE_VERT[pos_top]}"

    stelling_chessboard = ""

    for item in stelling_html.split(',,'):
        piece_info = item.split(",")
        piece_name = piece_info[0].split('_')[2].capitalize()
        piece_color = piece_info[0].split('_')[3]
        piece_pos = convert(int(piece_info[1]), int(piece_info[2]))

        stelling_chessboard += f"{piece_pos} {piece_color} {piece_name}\n"

    return cleanup_cb_stelling(stelling_chessboard.rstrip("\n"))


def convert_cb2html_stelling(stelling_chessboard):
    """Opposite conversion of convert_html2cb_stelling
    """

    stelling_html = ""

    for item in stelling_chessboard.split("\n"):
        piece_info = item.split()

        piece_pos_letter = piece_info[0][0]
        piece_pos_number = int(piece_info[0][1])
        piece_color = piece_info[1]
        piece_type = piece_info[2]

        piece_pos_left = str(CONVERT2LPOS[piece_pos_letter])
        piece_pos_top = str(CONVERT2TPOS[piece_pos_number])

        stelling_html += (f"{piece_type},{piece_color},{piece_pos_left},"
                          f"{piece_pos_top},{piece_pos_letter}{piece_pos_number},,")

    return stelling_html.rstrip(",").lower()


def load_cb_stelling(number):

    filepath = f'{MYPATH}/data/start_stellingen/stelling_{number}.txt'

    return read_stelling_data(filepath)


def write_cb_stelling(stelling_chessboard):

    with open(FILEPATH_CURRENT_GAME, 'w', encoding="utf-8") as file:
        file.write(stelling_chessboard)


class BasicGame():
    def __init__(self, init):

        if MOCK:

            self.game = TerminalGame(name="current_game",
                                       startsituation_file=FILEPATH_CURRENT_GAME, do_simulation=True,
                                       do_not_print_all_info=True, my_color = "white",
                                       current_color_to_play = 'white' if init else 'black',
                                       current_color_not_to_play = 'black' if init else 'white')

        else:

            self.game = TerminalGame(name="current_game", startsituation_file=FILEPATH_CURRENT_GAME,
                                       game_to_clone_from=False, do_simulation=True,
                                       do_not_print_all_info=True)
            self.game.my_color = "white"
            self.game.current_color_to_play = 'white' if init else 'black'
            self.game.current_color_not_to_play = 'black' if init else 'white'

        self.is_finished = False

    def _computer_makes_move(self):

        _ = self.game.move_pieces(move_nr=False, move=False, ai_level=1,
                         simulation=False, show_board=False)

    def _investigate_stelling(self):

        self.game.calculate_possible_moves()
        if self.game.current_possible_moves == {}:
            self.is_finished = True
            if self.game.check_check('King'):
                self.game.message = f'Checkmate: {self.game.current_color_not_to_play} has won'
            else:
                self.game.message = 'Stalemate'

    def _post_investigate_stelling(self):

        if self.game.check_check('King', self.game.current_color_not_to_play):
            self.game.message += 'Check!'

        pieces_on_board = sorted([piece.name for piece in self.game.pieces if piece.on_board])
        if pieces_on_board in [['King', 'King'],
                               ['King', 'King', 'Knight'],
                               ['Bishop', 'King', 'King']]:
            self.game.message = 'Stalemate'
            self.is_finished = True

        # analyse stelling from whites perspective

        self.game.current_color_to_play = 'white'
        self.game.current_color_not_to_play = 'black'

        self.game.calculate_possible_moves()
        if self.game.current_possible_moves == {}:
            self.is_finished = True
            if self.game.check_check('King'):
                self.game.message = f'Checkmate: {self.game.current_color_not_to_play} has won'
            else:
                self.game.message = 'Stalemate'

    def computer_plays(self):

        self._investigate_stelling()
        if not self.is_finished:
            self._computer_makes_move()
        self._post_investigate_stelling()

    def read_stelling(self):

        return self.game.show_board_simple(3)


class Game(db.Model):
    """nr_moves: 0,2,... -> whites turn  - 1,3,... -> blacks turn
    """

    id = db.Column(db.Integer(), primary_key=True)
    date = db.Column(db.String())
    result = db.Column(db.Text())
    nr_moves = db.Column(db.Integer())
    stelling_html = db.Column(db.Text())
    message = db.Column(db.Text())
    current_possible_moves = db.Column(db.Text())

    def __init__(self, startstelling_nr):

        self.date = datetime.datetime.now().strftime("%y-%m-%d %H:%M")
        self.nr_moves = 0
        self.result = ""
        self.message = 'Currently in mock mode: play: e2e4 d2d3 and then a random move' if MOCK else ''

        self.stelling_chessboard = load_cb_stelling(startstelling_nr)
        self.stelling_html = convert_cb2html_stelling(self.stelling_chessboard)

        self.current_possible_moves = self.__init_current_possible_moves()

    def __init_current_possible_moves(self):

        write_cb_stelling(self.stelling_chessboard)

        new_basic_game = BasicGame(init=True)
        new_basic_game.game.calculate_possible_moves()

        current_possible_moves = [value for key, value in new_basic_game.game.current_possible_moves.items()]
        return str({item[-1]:item[1] for item in current_possible_moves})

    def _computer_makes_move(self):
        """Export stelling to txt file in this format:
        h7 black Pawn
        e1 white Bishop
        ...

        Then initialise game in chess app simple with data from txt file.
        """

        write_cb_stelling(self.stelling_chessboard)

        new_basic_game = BasicGame(init=False)
        new_basic_game.computer_plays()

        self.stelling_chessboard = "\n".join(new_basic_game.read_stelling())

        self.message = new_basic_game.game.message
        if MOCK:
            self.message += 'Currently in mock mode: play: e2e4 d2d3 and then a random move'

        current_possible_moves = [value for key, value in new_basic_game.game.current_possible_moves.items()]
        self.current_possible_moves = str({item[-1]:item[1] for item in current_possible_moves})

    def update_stelling(self, stelling_html):

        self.nr_moves += 1

        self.stelling_chessboard = convert_html2cb_stelling(stelling_html)
        self._computer_makes_move()
        self.stelling_html = convert_cb2html_stelling(self.stelling_chessboard)
