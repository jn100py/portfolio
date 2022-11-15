# -*- coding: utf-8 -*-

import re

def read_stelling_data(filepath):
    """This function is also used in /chess_app_basic/chess_mock.py
    """
    
    with open(filepath, 'r', encoding="utf-8") as file:
        data = file.read()
        data = re.sub('\n\n\n*', '\n', data)

    return data.strip('\n')
