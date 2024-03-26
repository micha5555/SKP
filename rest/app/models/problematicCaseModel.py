from app.db import db
from app.extensions import getDatetimeNow, createDatetime

class ProblematicCase(db.Model):
    __tablename__ = 'problematic_case'
    id = db.Column(db.Integer, primary_key=True)
    registration_plate = db.Column(db.String(40), unique=False, nullable=False)
    detect_time = db.Column(db.DateTime, default=getDatetimeNow())
    localization = db.Column(db.String(22), unique=False, nullable=False)
    image = db.Column(db.String(56), unique=True, nullable=False)
    administration_edit_time = db.Column(db.DateTime, unique=False, nullable=True)
    probability = db.Column(db.Float(), unique=False, nullable=False)
    status = db.Column(db.String(4), unique=False, nullable=False)
    correction = db.Column(db.Boolean, unique=False, nullable=False)

    attr = ['register_plate', 'datetime', 'location', 'probability']
    attr_edit = ['registration', 'status']

    def __init__(self, registration, creation_time, localization, image, probability, status):
        self.registration_plate = registration
        self.detect_time = createDatetime(creation_time)
        self.localization = localization
        self.image = image
        self.probability = probability
        self.status = status
        self.correction = False

    def json(self):
        creation_time_formatted = self.detect_time.strftime('%Y-%m-%d %H:%M:%S')
        return {
			'id': self.id,
            'registration': self.registration_plate,
            'creation_time': creation_time_formatted,
            'localization': self.localization,
            'image': self.image,
            'probability': self.probability,
		}