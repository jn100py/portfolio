import os

STRING_FORMAT_DATETIME = '%Y %m %d %H:%M:%S'
STRING_FORMAT_DATETIME_2 = '%d %b %Y %H:%M:%S'  # example: 24 Sep 2022 18:13:55
STRING_FORMAT_DATE = '%Y %m %d'
STRING_FORMAT_TIMEZONE = '%Z%z'

MY_TIMEZONE = 'Europe/Amsterdam'


RSS_FEEDS = {

    'ad': [
        'https://www.ad.nl/binnenland/rss.xml',
        'https://www.ad.nl/buitenland/rss.xml',
        'https://www.ad.nl/politiek/rss.xml',
        'https://www.ad.nl/economie/rss.xml',
        'https://www.ad.nl/wetenschap/rss.xml',
],

    'nu': [
        'https://www.nu.nl/rss/Algemeen',
        'https://www.nu.nl/rss/Economie',
        'https://www.nu.nl/rss/Wetenschap',
        'https://www.nu.nl/rss/Tech',
        'https://www.nu.nl/rss/Gezondheid',
],

    'volkskrant': [
        'https://www.volkskrant.nl/voorpagina/rss.xml',
        'https://www.volkskrant.nl/nieuws-achtergrond/rss.xml',
        'https://www.volkskrant.nl/wetenschap/rss.xml',
        'https://www.volkskrant.nl/mensen/rss.xml',
        'https://www.volkskrant.nl/beter-leven/rss.xml',
        'https://www.volkskrant.nl/eten-en-drinken/rss.xml',
        'https://www.volkskrant.nl/werken/rss.xml',
        'https://www.volkskrant.nl/economie/rss.xml',
],

    'bbc': [
        'https://feeds.bbci.co.uk/news/uk/rss.xml',
],
}

NEWSPAPER2LANGUAGE = {'ad': 'NL',
                      'nu': 'NL',
                      'volkskrant': 'NL',
                      'bbc': 'EN',
                      }
NEWSPAPERS = list(NEWSPAPER2LANGUAGE.keys())

DEFAULT_NEWSPAPER = 'nu'

PROJECT_DIRECTORY = '/'.join(os.path.realpath(__file__).split('/')[0:-2])
DATA_DIRECTORY = f'{PROJECT_DIRECTORY}/data'

TESTMODE = False
