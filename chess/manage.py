import os
from flask_script import Manager
from chess_app import create_app
from chess_app.models import db, Game

env = os.environ.get('WEBAPP_ENV', 'dev')
app = create_app(f'chess_app.config.{env.capitalize()}Config')


if __name__ == "__main__":

    manager = Manager(app)

    @manager.shell
    def make_shell_context():
        return dict(
            app=app,
            db=db,
            Game=Game
        )

    manager.run()
