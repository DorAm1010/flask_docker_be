import os
from flask import Flask
from flask_migrate import Migrate
from pymongo import MongoClient
from pymongo.server_api import ServerApi

mongo_uri = os.getenv('MONGO_URI')
client = MongoClient(mongo_uri, server_api=ServerApi('1'))
db = client.healthpulse


def create_app():
    """Create and configure the flask application"""
    app = Flask(__name__)
    app.config['DATABASE_URI'] = '123'
    from routes import register_routes
    register_routes(app, db)
    migrate = Migrate(app, db)

    return app
