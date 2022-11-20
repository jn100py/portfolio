import json
from flask import Blueprint, render_template, abort, url_for, redirect, request, jsonify
from jinja2 import TemplateNotFound
from chess_app.models import db, Game


chess_blueprint = Blueprint('chess', __name__, template_folder='../templates')


@chess_blueprint.route('/')
def show():
    try:
        return render_template('home.html', init="home", game=False)
    except TemplateNotFound:
        abort(404)


@chess_blueprint.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', init="404", game=False)


@chess_blueprint.route('/new/<startstelling_nr>', methods=["GET"])
def start_new_game(startstelling_nr):

    new_game = Game(int(startstelling_nr))

    db.session.add(new_game)
    db.session.commit()

    return redirect(url_for("chess.show_game", gid=new_game.id))


@chess_blueprint.route('/game/<gid>', methods=["GET"])
def show_game(gid):

    current_game = Game.query.filter_by(id=int(gid)).first_or_404()

    #  initialise game
    current_possible_moves = eval(current_game.current_possible_moves)
    return render_template('game.html',
                           game_id=current_game.id,
                           stelling=current_game.stelling_html,
                           current_possible_moves=json.dumps(current_possible_moves),
                           init="game")


@chess_blueprint.route('/play/<gid>', methods=["POST"])
def play_game(gid):

    current_stelling = request.get_json("current_stelling")
    current_stelling = current_stelling['current_stelling'].rstrip(",")

    if current_stelling.startswith("-1"):  # when game ends

        result = current_stelling[2:]

        new_game = Game.query.filter_by(id=int(gid)).first_or_404()
        new_game.result = result
        db.session.commit()

        return jsonify()

    current_game = Game.query.filter_by(id=int(gid)).first_or_404()
    current_game.update_stelling(current_stelling)
    db.session.commit()

    current_possible_moves = eval(current_game.current_possible_moves)
    return jsonify(stelling=current_game.stelling_html,
                   nr_moves=str(current_game.nr_moves),
                   message=str(current_game.message),
                   current_possible_moves=json.dumps(current_possible_moves))


@chess_blueprint.route('/results')
def show_results():
    """ clean database : delete games with no end result
    """

    Game.query.filter_by(result='').delete()
    db.session.commit()

    games = Game.query.order_by(Game.date.desc()).all()
    return render_template('results.html', games=games, init="results", game=False)
