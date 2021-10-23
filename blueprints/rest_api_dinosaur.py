from database import Dinosaur, Game, db
from flask import Blueprint, jsonify, Response, request
import json


api = Blueprint(__name__, 'rest_api_dinosaur')


@api.route('/api/dinosaur', methods=['GET'])
def api_dinosaur() -> Response:
    if request.method.lower() == 'get':
        dinosaur_id = None

        try:
            # Try to get dinosaur id and dinosaur game id from request arguments:
            if 'id' in [*request.args.keys()]:
                dinosaur_id = request.args['id']

            if dinosaur_id is None:
                raise KeyError

        except KeyError:
            return jsonify({
                'status': 'error',
                'message': 'You must indicate the id of the dinosaur as a parameter.',
            })

        # Try to get the dinosaur by id:
        dinosaur = Dinosaur.query.get(dinosaur_id)
        if not dinosaur:
            return jsonify({
                'status': 'error',
                'message': f'Dinosaur {dinosaur_id} not found.'
            })

        return jsonify({
            "id": dinosaur.id,
            "game_id": dinosaur.game_id,
            "X": dinosaur.X,
            "Y": dinosaur.Y,
        })


@api.route('/api/dinosaur/delete', methods=['GET'])
def get_dinosaur() -> Response:
    if request.method.lower() == 'get':
        dinosaur_id = None

        try:
            # Try to get dinosaur id and dinosaur game id from request arguments:
            if 'id' in [*request.args.keys()]:
                dinosaur_id = request.args['id']

            if dinosaur_id is None:
                raise KeyError

        except KeyError:
            return jsonify({
                'status': 'error',
                'message': 'You must indicate the id of the dinosaur as a parameter.',
            })

        # Try to get the dinosaur by id:
        dinosaur = Dinosaur.query.get(dinosaur_id)
        if not dinosaur:
            return jsonify({
                'status': 'error',
                'message': f'Dinosaur {dinosaur_id} not found.'
            })

        # Get game of the dinosaur:
        game = Game.query.get(dinosaur.game_id)

        # Delete dinosaur from game dinosaurs json:
        game_dinosaurs: dict = json.loads(game.dinosaurs)
        game_dinosaurs.pop(str(dinosaur.id))
        game.dinosaurs = json.dumps(game_dinosaurs)

        # Delete dinosaur from database:
        db.session.delete(dinosaur)

        # Save changes:
        db.session.commit()

        return jsonify({
            'status': 'success',
            'message': f'Dinosaur {dinosaur_id} has been deleted successfully.'
        })
