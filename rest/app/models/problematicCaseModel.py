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

    attr = ['register_plate', 'datetime', 'location', 'image', 'probability', 'controller_id']
    attr_edit = ['id', 'registration', 'administration_edit_time', 'admin_id']
    attr_change = ['id', 'status']

    def __init__(self, registration, creation_time, localization, image, probability, status):
        self.registration_plate = registration
        self.detect_time = createDatetime(creation_time)
        self.localization = localization
        self.image = image
        self.probability = probability
        self.status = status
        self.correction = False

    def json(self):
        return {
			'id': self.id,
            'registratiom': self.registration,
            'creation_time': self.creation_time,
            'localization': self.localization,
            'image': self.image,
            'probability': self.probability,
		}