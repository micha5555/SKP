from flask import Flask
from config import Config
from app.db import db

def create_app(config = Config):
    app = Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)

    @app.route("/", methods=['GET'])
    def test():
        return "test"
    
    return app