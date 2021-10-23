from flask import Blueprint, render_template, Response, request


app = Blueprint(__name__, 'game_simulator_app')


@app.route('/', methods=['GET'])
def game() -> Response:
    return render_template('index.html')
