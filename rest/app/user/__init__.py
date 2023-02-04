from flask import Blueprint
bp = Blueprint('', __name__)
from app.user import routes