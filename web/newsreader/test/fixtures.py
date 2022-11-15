import pytest
import newsreader

from newsreader.config.constants import PROJECT_DIRECTORY
from newsreader.application.dictionary import Dictionary, Dictionaries


@pytest.fixture()
def dictionary():

    filepath_dictionary_en = PROJECT_DIRECTORY + '/test/data/dictionary_EN.txt'

    return Dictionary(filepath_dictionary_en)


@pytest.fixture()
def dictionaries(mocker):

    data_directory_test = PROJECT_DIRECTORY + '/test/data'
    mocker.patch.object(newsreader.application.dictionary, 'DATA_DIRECTORY', data_directory_test)

    return Dictionaries()
