#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask_sqlalchemy import SQLAlchemy
from typing import Any
from app import app
import json

db = SQLAlchemy(app)


class Robot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'))
    X = db.Column(db.Integer)
    Y = db.Column(db.Integer)


class Dinosaur(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'))
    X = db.Column(db.Integer)
    Y = db.Column(db.Integer)


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    grid_columns = db.Column(db.Integer)
    grid_rows = db.Column(db.Integer)
    robot_id = db.Column(db.Integer, db.ForeignKey('robot.id'))
    # dinosaurs: A string containing a JSON with all the dinosaurs of the game:
    dinosaurs = db.Column(db.String)

    @staticmethod
    def create_game(grid_cols: int, grid_rows: int, num_dinos: int, dinos_pos: list, robot_pos: list) -> Any:
        # Validating:
        if len(dinos_pos) != num_dinos:
            raise ValueError(
                'Dinosaurs positions array length must be equal to num_dinos')

        if grid_cols < 10 or grid_cols > 51:
            raise ValueError(
                'Grid columns must be greater than 10 and lower than 51')

        if grid_rows < 10 or grid_rows > 51:
            raise ValueError(
                'Grid rows must be greater than 10 and lower than 51')

        for dino_pos in dinos_pos:
            if dinos_pos.count(dino_pos) > 1:
                raise ValueError(
                    'Dinosaur position can not be repeated')
            if dino_pos[0] < 0 or dino_pos[0] >= grid_cols:
                raise ValueError(
                    'Dinosaur X position (Column) must be an integer number between 0 and ' + str(grid_cols - 1))
            if dino_pos[1] < 0 or dino_pos[1] >= grid_rows:
                raise ValueError(
                    'Dinosaur Y position (Row) must be an integer number between 0 and ' + str(grid_rows - 1))

        if robot_pos in dinos_pos:
            raise ValueError(
                'Two entities (Robot and dinosaurs) can not be in the same place')
        if len(robot_pos) != 2:
            raise ValueError(
                'The robot position must be a list containing the column and row where the robot will be placed. Example: robot_pos=[0, 1]'
            )
        if robot_pos[0] < 0 or robot_pos[0] >= grid_cols:
            raise ValueError(
                'Robot X position (Column) must be an integer number between 0 and ' + str(grid_cols - 1))
        if robot_pos[1] < 0 or robot_pos[1] >= grid_rows:
            raise ValueError(
                'Robot Y position (Row) must be an integer number between 0 and ' + str(grid_rows - 1))

        # Creating game:
        game = Game(grid_columns=grid_cols, grid_rows=grid_rows)
        robot = Robot(game_id=game.id, X=robot_pos[0], Y=robot_pos[1])
        dinos = [
            Dinosaur(game_id=game.id, X=dino_position[0], Y=dino_position[1])
            for dino_position in dinos_pos
        ]

        # Add new objects to the database session:
        for dino in dinos:
            db.session.add(dino)

        db.session.add(game)
        db.session.add(robot)

        # Save objects:
        db.session.commit()

        # Set game robot id and game dinosaur:
        game.robot_id = robot.id
        game.dinosaurs = json.dumps({
            dino.id: {
                "X": dino.X,
                "Y": dino.Y,
            } for dino in dinos
        })

        # Set robot game id and dinos game id:
        robot.game_id = game.id
        for dino in dinos:
            dino.game_id = game.id

        # Save changes:
        db.session.commit()

        return game


db.create_all()

if __name__ == '__main__':
    import doctest

    doctest.testfile('tests/test_database.rst', verbose=True)
