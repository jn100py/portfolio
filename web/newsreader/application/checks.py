from newsreader.config.constants import RSS_FEEDS, NEWSPAPERS, NEWSPAPER2LANGUAGE


def perform_startup_checks(dictionaries):

    if sorted(list(RSS_FEEDS.keys())) != sorted(NEWSPAPERS):
        print("\nERROR RSS_FEEDS\'s keys not in sync with NEWSPAPERS items"\
              "\nINFO  Check constants.py")
        return False

    dictionary_languages = [dictionary.language for dictionary in dictionaries.dictionaries]
    languages = list(set(NEWSPAPER2LANGUAGE.values()))
    if sorted(dictionary_languages) != sorted(2 * languages):
        print("\nERROR Incorrect configuration dictionaries"\
              "\nINFO  Check data folder"\
              "\nINFO  An exception dictionary might be absent")
        return False

    return True
