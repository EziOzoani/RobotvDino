from database import Dinosaur, Game, Robot, db
from random import randint
from flask import Blueprint, jsonify, Response, request
import config
import json


api = Blueprint(__name__, 'rest_api_game')


@api.route('/api/game/create', methods=['GET'])
def create_game() -> Response:
    # Creating game:
    game = Game()
    robot = Robot(game_id=game.id, X=randint(0, config.GRID_COLUMNS), Y=randint(0, config.GRID_COLUMNS))
    dinos = [Dinosaur(game_id=game.id, X=randint(0, config.GRID_COLUMNS), Y=randint(0, config.GRID_COLUMNS)) for i in range(5)]

    # Add new objects to the database session
    for dino in dinos:
        db.session.add(dino)

    db.session.add(game)
    db.session.add(robot)

    # Save objects:
    db.session.commit()


    # Cheack that two or more entities (robots or dinosaur) are not in the same position:
    dino_positions = []
    for dino in dinos:
        while any([dino.X in position and dino.Y in position for position in dino_positions]):
            dino.X = randint(0, config.GRID_COLUMNS)
            dino.Y = randint(0, config.GRID_ROWS)

        dino_positions.append((dino.X, dino.Y))

    # The robot and a dinosaur can not be in the same position
    while any([robot.X in position and robot.Y in position for position in dino_positions]):
        robot.X = randint(0, config.GRID_COLUMNS)
        robot.Y = randint(0, config.GRID_ROWS)

    print(dino_positions + [(robot.X, robot.Y)])

    # Set game robot id and game dinosaur:
    game.robot_id = robot.id
    game.dinosaurs = json.dumps({
        dino.id: {
            "X": dino.X,
            "Y": dino.Y,
        } for dino in dinos
    })

    # Set robot game id:
    robot.game_id = game.id

    # Set dinosaurs game id:
    for dino in dinos:
        dino.game_id = game.id

    # Save changes:
    db.session.commit()

    return jsonify({
        "id": game.id,
        "robot_id": game.robot_id,
        "dinosaurs": game.dinosaurs,
    })


@api.route('/api/game', methods=['GET'])
def get_game() -> Response:
    if request.method.lower() == 'get':
        game_id = None

        try:
            # Try to get game id or game robot id from request arguments:
            for param in ['id', 'robot_id']:
                if param in [*request.args.keys()]:
                    game_id = request.args[param]

            if game_id is None:
                raise KeyError

        except KeyError:
            return (
                '<a href="./game/create">Create game</a>'
            )

        # Try to get the game by id:
        game = Game.query.get(game_id)
        if not game:
            return jsonify({
                'status': 'error',
                'message': f'Game {game_id} not found.'
            })

        return jsonify({
            "id": game.id,
            "robot_id": game.robot_id,
            "dinosaurs": game.dinosaurs,
        })


@api.route('/api/game/delete', methods=['GET'])
def delete_game() -> Response:
    if request.method.lower() == 'get':
        game_id = None

        try:
            # Try to find game id or robot id in request arguments:
            for param in ['id', 'robot_id']:
                if param in [*request.args.keys()]:
                    game_id = request.args[param]

            if game_id is None:
                raise KeyError

        except KeyError:
            return jsonify({
                'status': 'error',
                'message': 'You must indicate the id of the game as a parameter.',
            })

        # Try to get the game by id:
        game = Game.query.get(game_id)
        if not game:
            return jsonify({
                'status': 'error',
                'message': f'Game {game_id} not found.'
            })

        # Delete instance:
        db.session.delete(game)
        db.session.commit()

        return jsonify({
            'status': 'success',
            'message': f'The Game {game_id} has been deleted successfully.',
        })
