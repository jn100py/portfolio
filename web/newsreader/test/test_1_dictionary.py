import pytest

from newsreader.test.fixtures import dictionary, dictionaries

"""To test Dictionary class:
    We use a fixture to load the file dictionary_EN.txt from /test/data/ in a Dictionary object

To test Dictionaries class:
    We use a fixture to load the dictionary files from /test/data in a Dictionaries object
    Therefor, we mock the constant DATA_DIRECTORY in dictionary.py and set it to value: <path2newsreader>/test/data/
"""


def test_initialize_dictionary(dictionary):

    assert dictionary.language == 'EN'
    assert dictionary.exception == False
    assert len(dictionary.single_words) == 2
    assert len(dictionary.sets_of_words) == 5


@pytest.mark.parametrize("words,text,result", [
                                        (['football', 'tennis'], "", 'tennis'),
                                        (['football', ':tennis:'], "", 'tennis'),
                                        ([], "A nice game on Roland Garros", "Roland Garros"),
                                        ([], "", False),
                                        (['football', 'darts'], "A nice movie on television.", False),
                                        ])
def test_dictionary_lookup(dictionary, words, text, result):
    
    assert dictionary.lookup(words, text) == result


def test_initialize_dictionaries(dictionaries):

    assert len(dictionaries.dictionaries) == 2


def test_find_dictionary(dictionaries):

    assert dictionaries.find_dictionary(language='EN', exception=False).language == 'EN'
    assert dictionaries.find_dictionary(language='EN', exception=True).language == 'EN'
    assert dictionaries.find_dictionary(language='NL') is False
    assert dictionaries.find_dictionary(language='NL', exception=4) is False
