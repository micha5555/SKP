from flask import Flask
from app.db import db
import os


def create_app():
    template_dir = os.path.abspath('app/public/templates')

    app = Flask(__name__)
    
    db.init_app(app)

    return app