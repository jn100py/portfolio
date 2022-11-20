import os
import pytest
import newsreader

import newsreader.application.dictionary
import newsreader.config.constants

from newsreader.application.datetime import fetch_local_datetime_info
from newsreader.application.entry import EntryFilter, read_news_entries, log_skipped_entries

from newsreader.config.constants import PROJECT_DIRECTORY

from newsreader.test.fixtures import dictionaries


@pytest.mark.parametrize("filter_on,title,summary,datetime_published_str,result_expected", [
                                        ("dict", "New elections announced in Ireland", "", "2021 11 06 11:21:34", [True, '']),
                                        ("dict", "New elections announced in Ireland", "", "2021 11 03 11:21:34", [False, 'not_in_date_range']),
                                        ("dict", "Federer wins Wimbledon", "A new title for Roger Federer ...", "2021 11 06 11:21:34", [False, 'filtered_by_dict']),
                                        ("dict", "Federer wins Wimbledon", "And also a new title for Roger Federer at the Olympics", "2021 11 06 11:21:34", [True, '']),
                                        ("only_date", "Federer wins Wimbledon", "A new title for Roger Federer ...", "2021 11 06 11:21:34", [True, '']),
                                        ])
def test_entry_filter(dictionaries, mocker, filter_on, title, summary, datetime_published_str, result_expected):

    mocker.patch.object(newsreader.application.datetime, 'TEST', 'Europe/Amsterdam')
    mocker.patch.object(newsreader.application.dictionary, 'DATA_DIRECTORY', f'{PROJECT_DIRECTORY}/test/data')

    local_datetime_info = fetch_local_datetime_info()

    entryfilter = EntryFilter(newspaper='bbc',
                              local_datetime_info=local_datetime_info,
                              filter_on=filter_on,
                              dictionaries=dictionaries)

    result, explanation = entryfilter.check(title, summary, datetime_published_str)

    assert [dictionary.language for dictionary in entryfilter.dictionaries.dictionaries] == ['EN', 'EN']
    assert entryfilter.language == 'EN'
    assert result == result_expected[0]
    assert explanation == result_expected[1]


def test_log_skipped_entries():

    entries_filtered = ['Some title']
    published_filtered = []

    log_skipped_entries(entries_filtered, published_filtered)


    lines_published = False
    lines_titles = False
    filepath_published = f'{PROJECT_DIRECTORY}/data/published_filtered.txt'
    filepath_titles = f'{PROJECT_DIRECTORY}/data/entries_filtered.txt'

    if os.path.isfile(filepath_published):
        with open(filepath_published, 'r', encoding="utf-8") as file:
            lines_published = file.readlines()
    if os.path.isfile(filepath_titles):
        with open(filepath_titles, 'r', encoding="utf-8") as file:
            lines_titles = file.readlines()

    assert lines_published == []
    assert lines_titles == ['Some title']


@pytest.mark.parametrize("filter_on,entries,result_expected", [
        ('dict',
         [],
         [0, 0, 0]),

        ('dict',
         [{'published': 'Sat, 6 Nov 2021 11:21:34 +0200',
               'title': 'New elections announced in Ireland',
             'summary': ''}],
         [1, 0, 0]),

        ('dict',
         [{'published': 'Mon, 1 Nov 2021 11:21:34 +0200',
               'title': 'New elections announced in Ireland',
             'summary': ''}],
         [0, 0, 0]),

        ('dict',
         [{'published': 'Sat, 6 Nov 2021 11:21:34 +0200',
               'title': 'Federer wins Wimbledon',
             'summary': 'A new title for Roger Federer ...'}],
         [0, 0, 1]),

        ('dict',
         [{'published': 'Sat, 6 Nov 2021 11:21:34 +0200',
               'title': 'Federer wins Wimbledon',
             'summary': 'And also a new title for Roger Federer at the Olympics'}],
         [1, 0, 0]),

        ('dict',
         [{
               'title': 'Federer wins Wimbledon',
             'summary': 'And also a new title for Roger Federer at the Olympics'}],
         [0, 1, 0]),

        ('dict',
         [{'published': 'Sat, 6 Nov 2021 11:21:34 +0200',
               'title': 'New elections announced in Ireland',
             'summary': ''},
          {'published': 'Sat, 6 Nov 2021 11:31:34 +0200',
               'title': 'Federer wins Wimbledon',
             'summary': 'And also a new title for Roger Federer at the Olympics'}],
         [2, 0, 0]),

        ('dict',
         [{'published': 'Sat, 6 Nov 2021 11:21:34 +0200',
               'title': 'New elections announced in Ireland',
             'summary': ''},
          {'published': 'Sat, 6 Nov 2021 11:31:34 +0200',
               'title': 'Federer wins Wimbledon',
             'summary': 'A new title for Roger Federer ...'}],
         [1, 0, 1]),

        ('only_date',
         [{'published': 'Sat, 6 Nov 2021 11:21:34 +0200',
               'title': 'New elections announced in Ireland',
             'summary': ''},
          {'published': 'Sat, 6 Nov 2021 11:31:34 +0200',
               'title': 'Federer wins Wimbledon',
             'summary': 'A new title for Roger Federer ...'}],
         [2, 0, 0]),

        ('only_date',
         [{'published': 'Sat, 6 Nov 2021 11:21:34 +0200',
               'title': 'New elections announced in Ireland',
             'summary': ''},
          {'published': 'Sat, 6 Nov 2021 11:21:34 +0200',
               'title': 'New elections announced in Ireland',
             'summary': ''}],
         [1, 0, 0]), # duplicate entry
    ])
def test_read_news_entries(dictionaries, mocker, filter_on, entries, result_expected):

    mocker.patch.object(newsreader.application.datetime, 'TEST', 'Europe/Amsterdam')
    mocker.patch.object(newsreader.application.dictionary, 'DATA_DIRECTORY', f'{PROJECT_DIRECTORY}/test/data')
    mocker.patch.object(newsreader.config.constants, 'RSS_FEEDS', {'bcc': ['someURL']})
    mocker.patch.object(newsreader.config.constants, 'MY_TIMEZONE', 'Europe/Amsterdam')

    mocker.patch("newsreader.application.entry.feedparser.parse", return_value={'entries': entries})

    local_datetime_info = fetch_local_datetime_info()
    entries2show, nr_entries_without_published, nr_entries_skipped =\
                    read_news_entries('bbc', filter_on, local_datetime_info, dictionaries)

    assert len(entries2show) == result_expected[0]
    assert nr_entries_without_published == result_expected[1]
    assert nr_entries_skipped == result_expected[2]


@pytest.mark.parametrize("filter_on,entries,result_expected", [
        ('dict',
         [{'published': 'Sat, 6 Nov 2021 11:21:34 +0200',
               'title': 'New elections announced in Ireland',
             'summary': ''}],
         [1, 0, 0]),

        ('dict',
         [{'published': 'Fri, 5 Nov 2021 19:00:00 +0200',
               'title': 'New elections announced in Ireland',
             'summary': ''}],
         [1, 0, 0]),

        ('dict',
         [{'published': 'Fri, 5 Nov 2021 18:59:59 +0200',
               'title': 'New elections announced in Ireland',
             'summary': ''}],
         [0, 0, 0]),

        ('dict',
         [{'published': 'Mon, 1 Nov 2021 11:21:34 +0200',
               'title': 'New elections announced in Ireland',
             'summary': ''}],
         [0, 0, 0]),

    ])
def test_read_news_entries_tz_jakarta(dictionaries, mocker, filter_on, entries, result_expected):

    mocker.patch.object(newsreader.application.datetime, 'TEST', 'Asia/Jakarta')
    mocker.patch.object(newsreader.application.dictionary, 'DATA_DIRECTORY', f'{PROJECT_DIRECTORY}/test/data')
    mocker.patch.object(newsreader.config.constants, 'RSS_FEEDS', {'bcc' : ['someURL']})
    mocker.patch.object(newsreader.config.constants, 'MY_TIMEZONE', 'Asia/Jakarta')

    mocker.patch("newsreader.application.entry.feedparser.parse", return_value={'entries': entries})

    local_datetime_info = fetch_local_datetime_info()
    entries2show, nr_entries_without_published, nr_entries_skipped =\
                                read_news_entries('bbc', filter_on, local_datetime_info, dictionaries)

    assert len(entries2show) == result_expected[0]
    assert nr_entries_without_published == result_expected[1]
    assert nr_entries_skipped == result_expected[2]
