import pytest
import newsreader

from newsreader.application.datetime import (_set_local_lower_boundary,
                                             convert_published_info2localtime,
                                             fetch_datetime_boundaries,
                                             fetch_local_datetime_info)


@pytest.mark.parametrize("datetime_last_visit,lower_bound,result", [
                                        ("2022 09 28 15:36:27", "2022 09 28 00:00:00", '2022 09 28 15:36:27'),
                                        ("2022 09 24 10:12:20", "2022 09 28 00:00:00", '2022 09 28 00:00:00'),
                                        ])
def test__set_local_lower_boundary(datetime_last_visit, lower_bound, result):

    assert _set_local_lower_boundary(datetime_last_visit, lower_bound) == result


def test_fetch_datetime_boundaries(mocker):
    """Constant 'TEST' is needed to bypass certain lines in datetime.py
    The line with datetime.now does not give constant outcomes, and the cookie
    cannot be read outside the context of the running Flask application. For now
    we don't test cookies.
    """

    mocker.patch.object(newsreader.application.datetime, 'TEST', 'Europe/Amsterdam')

    local_datetime_info = fetch_local_datetime_info()
    newspaper = 'some_newspaper'
    result_lower, result_upper = fetch_datetime_boundaries(newspaper, local_datetime_info)

    assert local_datetime_info.datetime_local_yesterday_str == '2021 11 05 00:00:00'
    assert local_datetime_info.utc_time_diff == 'CET+0100'
    assert result_lower == '2021 11 06 00:00:00'
    assert result_upper == '2021 11 06 23:59:59'


@pytest.mark.parametrize("published,utc_time_diff,result", [
                                        ("Sun, 25 Sep 2022 18:25:25 +0200", "+0200", '2022 09 25 18:25:25'),
                                        ("Sun, 25 Sep 2022 18:25:25 +0200", "+0700", '2022 09 25 23:25:25'),
                                        ("Sun, 25 Sep 2022 21:25:25 +0200", "+0700", '2022 09 26 02:25:25'),
                                        ("Sun, 25 Sep 2022 11:25:25 GMT", "-0400", '2022 09 25 07:25:25'),
                                        ])
def test_convert_published_info2localtime(published, utc_time_diff, result):

    assert convert_published_info2localtime(published, utc_time_diff) == result
