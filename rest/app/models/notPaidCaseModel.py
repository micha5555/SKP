from app.db import db
from app.models.userModel import User

class NotPaidCase(db.Model):
    __tablename__ = 'not_paid_case'
    id = db.Column(db.Integer, primary_key=True)
    registration_plate = db.Column(db.String(40), unique=False, nullable=False)
    detect_time = db.Column(db.String(21), unique=False, nullable=False)
    localization = db.Column(db.String(60), unique=False, nullable=False)
    image = db.Column(db.String(120), unique=False, nullable=False)

    attr = ['register_plate', 'datetime', 'location', 'probability']

    def __init__(self, registration, date, localization, filename):
        self.registration_plate = registration
        self.detect_time = date
        self.localization = localization
        self.image = filename

    def json(self):
        return {
			'id': self.id,
			'registration': self.registration_plate,
			'date': self.detect_time,
			'localization': self.localization,
			'filename': self.image,
		} 