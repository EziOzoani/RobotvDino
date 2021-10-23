from flask_sqlalchemy import SQLAlchemy
from app import app

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
    robot_id = db.Column(db.Integer, db.ForeignKey('robot.id'))
    # dinosaurs: A string containing a JSON with all the dinosaurs of the game:
    dinosaurs = db.Column(db.String)

db.create_all()
