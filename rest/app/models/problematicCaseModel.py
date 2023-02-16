from app.db import db

class ProblematicCase(db.Model):
    __tablename__ = 'problematic_case'
    id = db.Column(db.Integer, primary_key=True)
    registration = db.Column(db.String(40), unique=False, nullable=False)
    date = db.Column(db.DateTime, unique=False, nullable=False)
    localization = db.Column(db.String(60), unique=False, nullable=False)
    filename = db.Column(db.String(120), unique=False, nullable=False)
    correction = db.Column(db.String(10), unique=False, nullable=False)
    correction_date = db.Column(db.DateTime, unique=False, nullable=False)

    def __init__(self, registration, date, localization, filename):
        self.registration = registration
        self.date = date
        self.localization = localization
        self.filename = filename
        self.correction = False
        self.correction_date = False

    def json(self):
        return {
			'id': self.id,
			'registration': self.registration,
			'date': self.date,
			'localization': self.localization,
			'filename': self.filename,
            'correction': self.correction,
            'correction_date': self.correction_date
		}