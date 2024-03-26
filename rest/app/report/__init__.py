from flask import Blueprint
bp = Blueprint('report', __name__, url_prefix='/report')
from app.report import routes