from flask import Flask
from config import Config
from app.db import db

def create_app(config = Config):
    app = Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)

    from app.user import bp as user_bp
    app.register_blueprint(user_bp)
    
    from app.notPaidCase import bp as notPaidCaseBP
    app.register_blueprint(notPaidCaseBP)
    
    from app.problematicCase import bp as problematicCaseDB
    app.register_blueprint(problematicCaseDB)
    
    return app