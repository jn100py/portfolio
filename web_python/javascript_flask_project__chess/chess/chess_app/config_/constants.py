""" Contains conversion tables that are used to convert
HTML position of a piece to a chessboard position.

example of a chessboard position: a3

-

Furthermore: Conversion tables to convert chessboard position to HTML position.
Based on HTML alignment configuration.


This script is imported in models.py

also see alignment_settings in scripts.js
"""


POS_LEFT_RANGE = list(range(564, 2000, 86))[0:8]
CHESSBOARD_XRANGE = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

CONVERSION_TABLE_HOR = {item[0]:item[1] for item in zip(POS_LEFT_RANGE, CHESSBOARD_XRANGE)}

POS_TOP_RANGE = list(range(128, 2000, 86))[0:8]
CHESSBOARD_YRANGE = [8, 7, 6, 5, 4, 3, 2, 1]

CONVERSION_TABLE_VERT = {item[0]:item[1] for item in zip(POS_TOP_RANGE, CHESSBOARD_YRANGE)}


#


BOARD_HTML_TOFFSET = 128
BOARD_HTML_TWIDTH = 86

BOARD_HTML_LOFFSET = 564
BOARD_HTML_LWIDTH = 86


def calc_tpos(number):
    return BOARD_HTML_TOFFSET + BOARD_HTML_TWIDTH * number

def calc_lpos(number):
    return BOARD_HTML_LOFFSET + BOARD_HTML_LWIDTH * number

CONVERT2TPOS = {8 : calc_tpos(0),
                7 : calc_tpos(1),
                6 : calc_tpos(2),
                5 : calc_tpos(3),
                4 : calc_tpos(4),
                3 : calc_tpos(5),
                2 : calc_tpos(6),
                1 : calc_tpos(7)
                }

CONVERT2LPOS = {'a' : calc_lpos(0),
                'b' : calc_lpos(1),
                'c' : calc_lpos(2),
                'd' : calc_lpos(3),
                'e' : calc_lpos(4),
                'f' : calc_lpos(5),
                'g' : calc_lpos(6),
                'h' : calc_lpos(7)
                }


#


REL_PATH_CURRENT_GAME_FILE = '/data/current_game.txt'
