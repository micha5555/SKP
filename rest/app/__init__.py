from flask import Flask
from config import Config
# from app.db import db
# import json

def create_app(config = Config):
    app = Flask(__name__)
    app.config.from_object(config)
    # app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://root:root@172.23.23.23:3306/skp_test'
    # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # db.init_app(app)

    # @app.route("/test", methods=['GET'])
    # def test():
    #     return json.dumps("test")
    
    return app