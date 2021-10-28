import os

# Server configuration
TEMPLATE_FOLDER = 'public/templates'
STATIC_FOLDER = 'public/static'
DEBUG = True
HOST = '0.0.0.0'
PORT = 8000

# Database configuration
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.getcwd() + '/db.sqlite'
