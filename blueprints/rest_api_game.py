from database import Dinosaur, Game, Robot, db
from random import randint
from flask import Blueprint, jsonify, Response, request
import json


api = Blueprint(__name__, 'rest_api_game')


@api.route('/api/game/create', methods=['GET'])
def create_game() -> Response:
    # Getting game data:
    try:
        number_dinosaurs = request.args['num_dinos']
        grid_columns = request.args['grid_cols']
        grid_rows = request.args['grid_rows']
        dinos_pos = request.args['dinos_pos']
        robot_pos = request.args['robot_pos']
    except KeyError as error:
        return jsonify({
            'status': 'error',
            'message': '''
You must indicate the number of dinosaurs (num_dinos), dinosaurs positions in (dinos_pos: JSON format), 
grid columns (grid_cols), grid rows (grid_rows) and robot position (robot_pos: JSON format).
            '''.strip(),
        })

    # Check that the type of the data provided is valid:
    try:
        number_dinosaurs = int(number_dinosaurs)
    except ValueError:
        return jsonify({
            'status': 'error',
            'message': 'The number of dinosaurs must be an integer number.',
        })

    try:
        grid_columns = int(grid_columns)
    except ValueError:
        return jsonify({
            'status': 'error',
            'message': 'The number of grid columns must be an integer number.',
        })

    try:
        grid_rows = int(grid_rows)
    except ValueError:
        return jsonify({
            'status': 'error',
            'message': 'The number of grid rows must be an integer number.',
        })

    try:
        dinos_pos = json.loads(dinos_pos)
    except json.decoder.JSONDecodeError as error:
        return jsonify({
            'status': 'error',
            'message': 'An error ocurred while decoding dinosaurs JSON. ' + str(error),
        })

    try:
        robot_pos = json.loads(robot_pos)
    except json.decoder.JSONDecodeError as error:
        return jsonify({
            'status': 'error',
            'message': 'An error ocurred while decoding robot position JSON. ' + str(error),
        })

    # Check that the value of the data is valid:
    if grid_columns < 10 or grid_columns > 50:
        return jsonify({
            'status': 'error',
            'message': 'Grid columns must be greater than 9 and lower than 51.',
        })

    if grid_rows < 10 or grid_rows > 50:
        return jsonify({
            'status': 'error',
            'message': 'Grid rows must be greater than 9 and lower than 51.',
        })

    if number_dinosaurs < 1 or number_dinosaurs > grid_columns * grid_rows // 2:
        return jsonify({
            'status': 'error',
            'message': 'Number of dinosaurs must be greater than 0 and lower than ' +
            str(grid_columns * grid_rows // 2 + 1) +
            '.',
        })

    # If length of dinos positions list is not equal to number of dinosaurs:
    if len(dinos_pos) != number_dinosaurs:
        return jsonify({
            'status': 'error',
            'message': 'Dinosaurs positions array lenght has to be equal to num_dinos.',
        })
    for dino_pos in dinos_pos:
        if dino_pos[0] >= grid_columns or dino_pos[0] < 0:
            return jsonify({
                'status': 'error',
                'message': 'Dinosaurs position column must be an integer number between 0 and ' +
                str(grid_columns - 1) +
                '.',
            })
        if dino_pos[1] >= grid_rows or dino_pos[1] < 0:
            return jsonify({
                'status': 'error',
                'message': 'Dinosaurs position row must be an integer number between 0 and ' +
                str(grid_rows - 1) +
                '.',
            })

    # If robot position is lower than 2, the robot_pos list is not complete.
    # It must have 2 elements (X and Y).
    if len(robot_pos) < 2:
        return jsonify({
            'status': 'error',
            'message': 'Robot position argument must be a list containing the row and column where the robot will be placed.',
        })
    if robot_pos[0] >= grid_columns or robot_pos[0] < 0:
        return jsonify({
            'status': 'error',
            'message': 'Robot position column must be an integer number between 0 and ' +
            str(grid_columns - 1) +
            '.',
        })
    if robot_pos[1] >= grid_rows or robot_pos[1] < 0:
        return jsonify({
            'status': 'error',
            'message': 'Robot position row must be an integer number between 0 and ' +
            str(grid_rows - 1) +
            '.',
        })

    # Check dinos positions are not repeated:
    for index, dino_pos in enumerate(dinos_pos, 0):
        if dinos_pos.count(dino_pos) > 1:
            return jsonify({
                'status': 'error',
                'message': 'Error at dinosaurs positions array (Index: ' +
                str(index) +
                '). Two dinosaurs can not be in the same place.',
            })
    # Check robot position is not in dinos positions:
    if robot_pos in dinos_pos:
        return jsonify({
            'status': 'error',
            'message': 'Two entities (Robot or dinosaurs) can not be in the same place.',
        })

    # Create game:
    game = Game.create_game(grid_cols=grid_columns, grid_rows=grid_rows,
                            num_dinos=number_dinosaurs, dinos_pos=dinos_pos, robot_pos=robot_pos)

    return jsonify({
        'status': 'success',
        'id': game.id,
        'robot_id': game.robot_id,
        'dinosaurs': game.dinosaurs,
        'grid_columns': grid_columns,
        'grid_rows': grid_rows,
    })


@api.route('/api/game', methods=['GET'])
def get_game() -> Response:
    if request.method.lower() == 'get':
        game_id = None

        try:
            # Try to get game id from request arguments:
            if 'id' in [*request.args.keys()]:
                game_id = request.args['id']

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
                'message': 'Game ' + str(game_id) + ' not found.'
            })

        return jsonify({
            'status': 'success',
            'id': game.id,
            'robot_id': game.robot_id,
            'dinosaurs': game.dinosaurs,
            'grid_columns': game.grid_columns,
            'grid_rows': game.grid_rows,
        })


@api.route('/api/game/delete', methods=['GET'])
def delete_game() -> Response:
    if request.method.lower() == 'get':
        try:
            # Try to find the id of the game in request arguments:
            if 'id' in [*request.args.keys()]:
                game_id = request.args['id']

        except KeyError:
            return jsonify({
                'status': 'error',
                'message': 'You must indicate the id of the game as a parameter.',
            })

        # Try to get the game by its id:
        game = Game.query.get(game_id)
        if not game:
            return jsonify({
                'status': 'error',
                'message': 'Game ' + str(game_id) + ' not found.'
            })

        # Get game dinosaurs:
        dinosaurs = json.loads(game.dinosaurs)

        # Delete game instance and dependent instances:
        # Delete dinosaurs:
        for dinosaur in dinosaurs:
            db.session.delete(Dinosaur.query.get(dinosaur))
        # Delete game robot:
        db.session.delete(Robot.query.get(game.robot_id))
        # Delete game:
        db.session.delete(game)
        # Save changes:
        db.session.commit()

        return jsonify({
            'status': 'success',
            'message': 'The Game ' + str(game_id) + ' has been deleted successfully.',
        })
