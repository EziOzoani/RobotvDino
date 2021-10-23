#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask_cors import CORS
from flask import Response
from app import app
import config


# Usefull functions
def after_request(response: Response) -> Response:
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')

    return response


# CORS Settings:
cors = CORS(app, resources={
    r'/api/*': {
        'origins': '*'
    }
})


# Register blueprints
from blueprints.tests.game_simulator import app as game_simulator_app
from blueprints.rest_api_dinosaur import api as rest_api_dinosaur
from blueprints.rest_api_robot import api as rest_api_robot
from blueprints.rest_api_game import api as rest_api_game

rest_api_dinosaur.after_request(after_request)
rest_api_robot.after_request(after_request)
rest_api_game.after_request(after_request)

app.register_blueprint(game_simulator_app)
app.register_blueprint(rest_api_dinosaur)
app.register_blueprint(rest_api_robot)
app.register_blueprint(rest_api_game)


# First routes
@app.route('/api/', methods=['GET'])
def api() -> Response:
    return (
        '<a href="./robot">Robot</a>\n'
        '<a href="./dinosaur">dinosaur</a>\n'
        '<a href="./game">Game</a>'
    )


# Allow cross origin:
app.after_request(after_request)


# Main function
def main() -> None:
    app.run(config.HOST, config.PORT, debug=config.DEBUG)

    if config.DEBUG:
        # Clean database:
        print('', file=open('db.sqlite', 'w'))


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\b\b  \nExit...')
        exit(0)
