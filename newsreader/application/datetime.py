import datetime
import pytz
from flask import request

from newsreader.config.constants import STRING_FORMAT_DATETIME, STRING_FORMAT_DATE,\
                                        STRING_FORMAT_DATETIME_2, STRING_FORMAT_TIMEZONE,\
                                        MY_TIMEZONE
TEST = False

"""
TEST   is used by pytest, contains string with timezone name

"""


def fetch_local_datetime_info():
    """DateTimeLocal needs to be set with most recent / actual datetime information,
    therefor the class definition was put inside a function, which is called
    everytime the browser is refreshed.

    Uses datetime.datetime.now

    UTC
        Coordinated Universal Time
        replaced GMT (Greenwich Mean Time)

    CET
        Central European Time
        UTC+1

    CEST
        Central European Summer Time
        UTC+2

    common values for utc_time_diff : CET+0100, CEST+0200
    """

    class DateTimeLocal():
        datetime_local_current = datetime.datetime.now(pytz.timezone(MY_TIMEZONE))
        if TEST:
            timezone = pytz.timezone(f'{TEST}')
            datetime_now_local_test_str = '2021 11 06 12:21:28'
            datetime_local_current = datetime.datetime.strptime(datetime_now_local_test_str,
                                                                STRING_FORMAT_DATETIME)
            datetime_local_current = timezone.localize(datetime_local_current)

        datetime_local_current_str = datetime_local_current.strftime(STRING_FORMAT_DATETIME)
        date_local_current_str = datetime_local_current.strftime(STRING_FORMAT_DATE)

        datetime_local_yesterday = datetime_local_current - datetime.timedelta(days=1)
        datetime_local_yesterday_str = datetime_local_yesterday.strftime(STRING_FORMAT_DATE) + ' 00:00:00'

        utc_time_diff = datetime_local_current.strftime(STRING_FORMAT_TIMEZONE)

    return DateTimeLocal


def _get_datetime_last_visit(newspaper):

    cookie_contents = request.cookies.get(newspaper) if TEST is False else ""
    if cookie_contents:
        datetime_last_visit = cookie_contents
        return datetime_last_visit

    return ""

def _set_local_lower_boundary(datetime_last_visit, lower_bound):

    if datetime_last_visit < lower_bound:
        return lower_bound

    return datetime_last_visit

def fetch_datetime_boundaries(newspaper, local_datetime_info):

    datetime_last_visit = _get_datetime_last_visit(newspaper)
    no_cookie = not bool(datetime_last_visit)
    if no_cookie:
        local_datetime_lower_bound = local_datetime_info.date_local_current_str + ' 00:00:00'

    else:
        local_datetime_lower_bound = _set_local_lower_boundary(datetime_last_visit,
                                                         lower_bound=local_datetime_info.datetime_local_yesterday_str)

    local_datetime_upper_bound = f'{local_datetime_info.date_local_current_str} 23:59:59'

    return local_datetime_lower_bound, local_datetime_upper_bound


def convert_published_info2localtime(published, utc_time_diff):
    """Datetime of a newsentry is here converted to a datetime in the timezone
    set by the user (see constants.py).

    Example values:
    for published
        Sun, 25 Sep 2022 18:25:25 +0200
        Sun, 25 Sep 2022 18:25:25 GMT
    """

    _, *datetime_published, timezone_message = published.split(' ')
    datetime_published_str = " ".join(datetime_published)

    datetime_published = datetime.datetime.strptime(datetime_published_str,
                                                    STRING_FORMAT_DATETIME_2)


    utc_delta = int(utc_time_diff[-5:].replace('0', ''))
    utc_delta_message = 0 if timezone_message == 'GMT' else int(timezone_message.replace('0', ''))

    hours2add = utc_delta - utc_delta_message


    datetime_published_shifted = datetime_published + datetime.timedelta(hours=hours2add)
    datetime_published_shifted_str = datetime_published_shifted.strftime(STRING_FORMAT_DATETIME)

    return datetime_published_shifted_str
