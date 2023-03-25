from flask import Blueprint
bp = Blueprint('notPaidCase', __name__, url_prefix='/notPaidCase')
from app.notPaidCase import routes