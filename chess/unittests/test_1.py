import pytest
from urllib.request import urlopen

from selenium import webdriver

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait


def test_index(client):
    """Start website
    Check if Play Chess! is being displayed.
    """

    response = client.get("/")

    assert b"Play Chess!" in response.data


def test_results(client):
    """Open results page
    Check if Results is being displayed
    """

    response = client.get("/results")

    assert b"Results" in response.data


def test_new_game_startstelling_1(client):
    """Start new game (startstelling 1).
    Check if the number of pieces is equal to 32
    """

    response = client.get("/new/1", follow_redirects=True)

    assert 32 == response.data.decode('utf-8').count('<img id="img_piece_')


def test_new_game_startstelling_3(client):
    """Start new game (startstelling 3).
    Check if the number of pieces is equal to 6
    Result also in 32 as JavaScript initialisation functions are not executed.
    """

    response = client.get("/new/3")

    url = response.headers['Location']
    url_part = "/" + "/".join(url.split('/')[-2:])
    url = "http://127.0.0.1:5000" + url_part
    res = urlopen(url)

    assert 32 == res.read().decode('utf-8').count('<img id="img_piece_')


@pytest.fixture()
def browser(request):
    opts = Options()
    opts.headless = True
    driver = Firefox(options=opts)

    driver.implicitly_wait(10)

    yield driver

    driver.quit()


def test_a_check_main_text(browser):
    """Start website
    Check if Play Chess! is being displayed.
    """

    browser.get("http://127.0.0.1:5000")

    element = browser.find_element(by=By.XPATH, value="//h1")

    assert element.text == 'Play Chess!'


def test_b_move_white_pawn_e2(browser):
    """Load startstelling 1.
    Move white Pawn from e2 to e5.
    Check if it still on e2.
    Move white Pawn from e2 to e4.
    Check if it has been moved to e4.
    """

    browser.get("http://127.0.0.1:5000")

    element = browser.find_element(by=By.XPATH, value="//a[@href='/new/1']")
    element.click()

    WebDriverWait(browser, 2)

    assert browser.current_url.startswith('http://127.0.0.1:5000/game/')


    element = browser.find_element(by=By.ID, value="img_piece_pawn_white_5")

    assert element.get_attribute("style") == "left: 908px; top: 644px;"


    ActionChains(browser).drag_and_drop_by_offset(element, 0, -258).perform()

    assert element.get_attribute("style") == "left: 908px; top: 644px;"


    ActionChains(browser).drag_and_drop_by_offset(element, 0, -172).perform()

    assert element.get_attribute("style") == "left: 908px; top: 472px;"


def test_c_move_white_queen(browser):
    """Load startstelling 3 which contains 6 pieces.
    Move white queen from a2 to a8 and press the Move button.
    Check if white queen is on a8.
    """

    browser.get("http://127.0.0.1:5000/new/3")

    WebDriverWait(browser, 2)

    assert browser.current_url.startswith('http://127.0.0.1:5000/game/')


    elements = browser.find_elements(by=By.XPATH, value="//img[contains(@id,'img_piece_')]")

    assert len(elements) == 6


    element = browser.find_element(by=By.ID, value="img_piece_queen_white_1")

    ActionChains(browser).drag_and_drop_by_offset(element, 0, -516).perform()

    assert element.get_attribute("style") == "left: 564px; top: 128px;"


    current_url = browser.current_url

    element = browser.find_element(by=By.XPATH, value="//button[text() = 'Move']")

    element.click()

    WebDriverWait(browser, 5)

    browser.get(current_url) # refresh ...

    element = browser.find_element(by=By.ID, value="img_piece_queen_white_1")

    assert element.get_attribute("data-origpos") == "a8"
