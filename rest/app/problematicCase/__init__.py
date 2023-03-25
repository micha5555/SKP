from flask import Blueprint
bp = Blueprint('problematicCase', __name__, url_prefix='/problematicCase')
from app.problematicCase import routes