import sys
import os
import pytest

MYPARENTPATH = '/'.join(os.path.realpath(__file__).split('/')[0:-2])
sys.path.append(MYPARENTPATH)

from chess_app import create_app

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""

    env = "test"
    app = create_app(f'chess_app.config.{env.capitalize()}Config')

    yield app


@pytest.fixture
def client(app):
    return app.test_client()
