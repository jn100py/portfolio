import feedparser

from newsreader.application.datetime import convert_published_info2localtime,\
                                            fetch_datetime_boundaries
from newsreader.config.constants import RSS_FEEDS, NEWSPAPER2LANGUAGE, DATA_DIRECTORY


class EntryFilter():
    def __init__(self, newspaper, local_datetime_info, filter_on, dictionaries):

        self.local_datetime_lower_bound, self.local_datetime_upper_bound =\
                                        fetch_datetime_boundaries(newspaper,
                                                                  local_datetime_info)

        self.language = NEWSPAPER2LANGUAGE[newspaper]
        self.filter_on = filter_on
        self.dictionaries = dictionaries

        self.match_in_dict = False

    def check(self, title, summary, datetime_published_str):

        text = f"{title} {summary}"
        words = text.split()

        in_date_range = False

        if self.local_datetime_lower_bound <= datetime_published_str <= self.local_datetime_upper_bound:
            in_date_range = True

        if not in_date_range:
            return False, 'not_in_date_range'


        if self.filter_on == 'only_date':
            return True, ''

        if self.filter_on == 'dict':
            result_lookup = self.dictionaries.find_dictionary(self.language).lookup(words, text)
            if result_lookup is False:
                return True, ''

            result_lookup_except = self.dictionaries.find_dictionary(self.language, exception=True).lookup(words, text)
            if result_lookup_except:
                return True, ''

            self.match_in_dict = result_lookup  # will be written to entries_filtered.txt

        return False, 'filtered_by_dict'


def read_news_entries(newspaper, filter_on, local_datetime_info, dictionaries):

    entries2show = []
    entries2show_titles = []

    entries_filtered = []
    published_filtered = []

    nr_entries_without_published = 0
    nr_entries_skipped = 0

    entry_filter = EntryFilter(newspaper, local_datetime_info, filter_on, dictionaries)

    for rss_feed in RSS_FEEDS[newspaper]:
        for entry in feedparser.parse(rss_feed)['entries']:

            if 'published' not in entry:
                nr_entries_without_published += 1
                continue


            title = entry['title']
            summary = entry['summary']

            if title in entries2show_titles:  # In case of duplicate entries
                continue


            published = entry['published']
            datetime_published_localtime_str =\
                        convert_published_info2localtime(published,
                                                         local_datetime_info.utc_time_diff)


            filter_passed, reason_not_added =\
                        entry_filter.check(title,
                                           summary,
                                           datetime_published_localtime_str)
            if filter_passed:

                entries2show.append(entry)
                entries2show_titles.append(title)

            else:

                if reason_not_added == 'filtered_by_dict':
                    match_in_dict = entry_filter.match_in_dict
                    entries_filtered.append(f"\n\n{title}\n{summary}\n"\
                                            f"filtered on: {match_in_dict}".replace('. ', '.\n'))
                    nr_entries_skipped += 1

                elif reason_not_added == 'not_in_date_range':
                    published_filtered.append(published)

    entries2show.sort(key=lambda entry: entry['published'])

    log_skipped_entries(entries_filtered, published_filtered)

    return entries2show, nr_entries_without_published, nr_entries_skipped


def log_skipped_entries(entries_filtered, published_filtered):

    filepath_entries_filtered = f'{DATA_DIRECTORY}/entries_filtered.txt'
    filepath_published_filtered = f'{DATA_DIRECTORY}/published_filtered.txt'

    with open(filepath_entries_filtered, 'w', encoding="utf-8") as file:
        file.write("\n".join(entries_filtered))

    with open(filepath_published_filtered, 'w', encoding="utf-8") as file:
        file.write("\n".join(published_filtered))
