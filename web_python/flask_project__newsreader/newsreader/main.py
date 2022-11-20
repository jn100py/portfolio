import datetime
import sys

from flask import Flask
from flask import render_template
from flask import redirect
from flask import make_response

from newsreader.application.dictionary import Dictionaries
from newsreader.application.datetime import fetch_local_datetime_info
from newsreader.application.entry import read_news_entries
from newsreader.application.checks import perform_startup_checks

from newsreader.config.constants import NEWSPAPERS, TESTMODE, DEFAULT_NEWSPAPER

dictionaries = Dictionaries()
errors_reported = perform_startup_checks(dictionaries)
if errors_reported is False:
    print('\nINFO  Exiting')
    sys.exit()
else:
    app = Flask(__name__)
    app.secret_key = "Gxf613UhGRkzAKd47R5daLrUelnlUL4L6AU4z0uu++TNBpdzhAolufHqPQiiEdn34pbE97bmXbN"


@app.route("/")
def get_news(newspaper=f'{DEFAULT_NEWSPAPER}', filter_on='dict'):

    local_datetime_info = fetch_local_datetime_info()
    entries2show, nr_entries_without_published, nr_entries_skipped =\
                    read_news_entries(newspaper, filter_on, local_datetime_info, dictionaries)
    if TESTMODE:
        entries2show = entries2show[:4]


    response = make_response(render_template("home.html",
                                             articles=entries2show,
                                             nr_articles_filtered=nr_entries_skipped,
                                             nr_entries_without_published=nr_entries_without_published))

    if TESTMODE:
        return response

    expires = local_datetime_info.datetime_local_current + datetime.timedelta(days=15)
    response.set_cookie(newspaper, local_datetime_info.datetime_local_current_str, expires=expires)

    return response


@app.route("/<newspaper>")
def get_news_today(newspaper):

    if newspaper in NEWSPAPERS:
        return get_news(newspaper=newspaper)
    return redirect("/")


@app.route("/nofilter/<newspaper>")
def get_news_today_not_filtered(newspaper):

    if newspaper in NEWSPAPERS:
        return get_news(newspaper=newspaper, filter_on='only_date')
    return redirect("/")


if __name__ == "__main__":
    app.run(port=5000, debug=True)
