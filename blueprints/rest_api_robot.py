from database import Dinosaur, Game, Robot, db
from flask import Blueprint, jsonify, Response, request
import config
import json


api = Blueprint(__name__, 'rest_api_robot')


@api.route('/api/robot', methods=['GET'])
def get_robot() -> Response:
    if request.method.lower() == 'get':
        robot_id = None

        try:
            # Try to get robot id and robot game id from request arguments:
            for param in ['id', 'game_id']:
                if param in [*request.args.keys()]:
                    robot_id = request.args[param]

            if robot_id is None:
                raise KeyError

        except KeyError:
            return jsonify({
                'status': 'error',
                'message': 'You must indicate the id of the robot as a parameter.',
            })

        # Try to get the robot by id:
        robot = Robot.query.get(robot_id)
        if not robot:
            return jsonify({
                'status': 'error',
                'message': f'Robot {robot_id} not found.'
            })

        return jsonify({
            "id": robot.id,
            "game_id": robot.game_id,
            "X": robot.X,
            "Y": robot.Y,
        })


@api.route('/api/robot/move', methods=['GET'])
def move_robot() -> Response:
    if request.method.lower() == 'get':
        allowed_params = ['id', 'direction']
        params = [*request.args.keys()]

        # If there is a missing parameter, it returns an error:
        if any([not param in params for param in allowed_params]):
            return jsonify({
                'status': 'error',
                'message': 'You must indicate the id of the robot, and the direction to which it will move as parameters.',
            })

        # Try to get the robot by id
        robot_id = request.args['id']
        robot = Robot.query.get(robot_id)
        if not robot:
            return jsonify({
                'status': 'error',
                'message': f'Robot {robot_id} not found.',
            })

        # Get the robot game:
        game = Game.query.get(robot.game_id)

        # Get game dinosaurs:
        dinosaurs = json.loads(game.dinosaurs)

        # Change the position of the robot:
        direction = request.args['direction']
        if direction == 'left' and robot.X > 0:
            for dinosaur in dinosaurs:
                if robot.X - 1 == dinosaurs[dinosaur]['X'] and \
                    robot.Y == dinosaurs[dinosaur]['Y']:
                    return jsonify({
                        'status': 'error',
                        'message': 'The space to which the robot was tried to move is already being occupied.',
                    })

            robot.X -= 1
        elif direction == 'right' and robot.X < config.GRID_COLUMNS:
            for dinosaur in dinosaurs:
                if robot.X + 1 == dinosaurs[dinosaur]['X'] and \
                    robot.Y == dinosaurs[dinosaur]['Y']:
                    return jsonify({
                        'status': 'error',
                        'message': 'The space to which the robot was tried to move is already being occupied.',
                    })

            robot.X += 1
        elif direction == 'front' and robot.Y > 0:
            for dinosaur in dinosaurs:
                if robot.Y - 1 == dinosaurs[dinosaur]['Y'] and \
                    robot.X == dinosaurs[dinosaur]['X']:
                    return jsonify({
                        'status': 'error',
                        'message': 'The space to which the robot was tried to move is already being occupied.',
                    })

            robot.Y -= 1
        elif direction == 'behind' and robot.Y < config.GRID_ROWS:
            for dinosaur in dinosaurs:
                if robot.Y + 1 == dinosaurs[dinosaur]['Y'] and \
                    robot.X == dinosaurs[dinosaur]['X']:
                    return jsonify({
                        'status': 'error',
                        'message': 'The space to which the robot was tried to move is already being occupied.',
                    })

            robot.Y += 1
        else:
            return jsonify({
                'status': 'error',
                'message': 'Invalid direction.',
            })

        # Save changes:
        db.session.commit()

        return jsonify({
            'status': 'success',
            'message': 'The robot has been moved successfully.',
        })


@api.route('/api/robot/attack', methods=['GET'])
def robot_attack() -> Response:
    if request.method.lower() == 'get':
        allowed_params = ['id', 'game_id']
        params = [*request.args.keys()]

        # If there is a missing parameter, it returns an error:
        if not any([param in params for param in allowed_params]):
            return jsonify({
                'status': 'error',
                'message': 'You must indicate the id of the robot or the id of its game.',
            })

        # Try to get the robot by id
        robot_id = request.args['id'] if 'id' in params else request.args['game_id']
        robot = Robot.query.get(robot_id)
        if not robot:
            return jsonify({
                'status': 'error',
                'message': f'Robot {robot_id} not found.',
            })

        # Get game of the robot:
        game = Game.query.get(robot.game_id)

        # Get dinosaurs around the robot:
        removed_dinosaurs_id = []
        dinosaurs = json.loads(game.dinosaurs)

        # Delete dinosaurs around
        for dinosaur_id in dinosaurs:
            dino_position = dinosaurs[dinosaur_id]

            if dino_position['X'] + 1 == robot.X and dino_position['Y'] == robot.Y or \
                dino_position['X'] - 1 == robot.X and dino_position['Y'] == robot.Y or \
                dino_position['Y'] + 1 == robot.Y and dino_position['X'] == robot.X or \
                dino_position['Y'] - 1 == robot.Y and dino_position['X'] == robot.X:
                # Append the id of the dinosaur for remove it later from the game dinosaurs json:
                removed_dinosaurs_id.append(dinosaur_id)

                # Delete dino in database
                db.session.delete(Dinosaur.query.get(dinosaur_id))

        for removed_dinosaur_id in removed_dinosaurs_id:
            # Delete dinosaur from game dinosaurs json:
            del dinosaurs[removed_dinosaur_id]

        # Reset game dinosaurs json:
        game.dinosaurs = json.dumps(dinosaurs)

        # Save changes
        db.session.commit()

        return jsonify({
            'status': 'success',
            'message': 'Dinosaurs around the robot has been removed successfully.',
        })
