import re
import os
import string

from newsreader.config.constants import DATA_DIRECTORY

REGEX_DATAFILE = r'/.*/dictionary_([A-Z]{2,3})(_(exception)){0,1}\.txt'
PUNCTUATION = string.punctuation + "‘’"


class Dictionary():
    def __init__(self, filepath):

        self.filepath = filepath

        language, _, type_ = re.match(REGEX_DATAFILE, filepath).groups()
        self.language = language
        self.exception = type_ == 'exception'

        self.single_words = False
        self.sets_of_words = False

        self._read_data()

    def _read_data(self):

        with open(self.filepath, 'r', encoding="utf-8") as file:
            lines = [line.strip() for line in file.readlines() if line.strip()]

        self.single_words = [line.lower() for line in lines if ' ' not in line]
        self.sets_of_words = [line for line in lines if ' ' in line]

    def lookup(self, words, text):

        for word in words:
            stripped_word = word.strip(PUNCTUATION).lower()
            if stripped_word in self.single_words:
                return stripped_word

        for set_ in self.sets_of_words:
            if set_ in text:
                return set_

        return False


class Dictionaries():
    def __init__(self):
        self.dictionaries = []

        self._add_dictionaries()

    def _add_dictionaries(self):

        for filename in os.listdir(DATA_DIRECTORY):

            filepath = DATA_DIRECTORY + '/' + filename
            if re.match(REGEX_DATAFILE, filepath):
                new_dictionary = Dictionary(filepath)
                self.dictionaries.append(new_dictionary)

    def find_dictionary(self, language, exception=False):

        for dictionary in self.dictionaries:
            if dictionary.language == language and dictionary.exception is exception:
                return dictionary

        return False
