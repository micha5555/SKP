from flask import Flask
from config import Config
from app.db import db
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
CORS(app)
app.config['CORS_ALLOW_ALL_ORIGINS'] = True

from app.user import bp as user_bp
app.register_blueprint(user_bp)

from app.notPaidCase import bp as notPaidCaseBP
app.register_blueprint(notPaidCaseBP)

from app.problematicCase import bp as problematicCaseDB
app.register_blueprint(problematicCaseDB)

from app.report import bp as reportBP
app.register_blueprint(reportBP)
