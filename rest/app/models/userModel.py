from json import dumps
from datetime import datetime
from werkzeug.security import generate_password_hash
from app.db import db
from app.models.problematicCaseModel import ProblematicCase
from app.models.reportModel import Report
from app.models.connectors import user_not_paid_case_association, user_problematic_case_association

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(40), unique=False, nullable=False)
    last_name = db.Column(db.String(40), unique=False, nullable=False)
    login = db.Column(db.String(40), unique=True, nullable=False)
    password = db.Column(db.String(255), unique=False, nullable=False)
    is_admin = db.Column(db.Boolean, unique=False, default=False)
    is_controller = db.Column(db.Boolean, unique=False, default=False)

    not_paid_cases = db.relationship('NotPaidCase', secondary=user_not_paid_case_association, backref='users')
    problematic_cases = db.relationship('ProblematicCase', secondary=user_problematic_case_association, backref='users')

    attr = ['first_name', 'last_name', 'login', 'password', 'is_admin', 'is_controller']
    attr_edit = ['first_name', 'last_name', 'login', 'is_admin', 'is_controller']
    loginAttr = ['login', 'password']

    def __init__(self, first_name, last_name, login, password, is_admin=False, is_controller=False):
        self.first_name = first_name
        self.last_name = last_name
        self.login = login
        self.password = generate_password_hash(password)
        self.is_admin = is_admin
        self.is_controller = is_controller

    def json(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'login': self.login,
            'is_admin': self.is_admin,
            'is_controller': self.is_controller,
        }

    def generatePayload(self):
        now=datetime.now().isoformat()
        return {
            'login': self.login,
            'id': self.id,
            'is_admin': self.is_admin,
            'is_controller':  self.is_controller,
            'current_time': dumps(now)
        }