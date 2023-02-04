from flask import Blueprint
bp = Blueprint('notPaidCase', __name__)
from app.notPaidCase import routes