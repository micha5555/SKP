from flask import Flask
from app.db import db
import json

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///app.db'
    db.init_app(app)

    @app.route("/test", methods=['GET'])
    def test():
        return json.dumps("test")
    
    return app