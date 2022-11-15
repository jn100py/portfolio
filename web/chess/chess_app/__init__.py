#!/usr/bin/env python

from flask import Flask
from .models import db
from .controllers.controllers import chess_blueprint


def create_app(object_name):

    app = Flask(__name__)
    app.config.from_object(object_name)

    db.init_app(app)

    app.register_blueprint(chess_blueprint)

    return app


if __name__ == '__main__':
    app = app = create_app()
    app.run()
