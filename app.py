from flask import Flask
import config
import os

# Create a Flask app, and create a random secret key:
app = Flask(__name__, template_folder=config.TEMPLATE_FOLDER,
            static_folder=config.STATIC_FOLDER)
app.secret_key = os.urandom(32)
app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
