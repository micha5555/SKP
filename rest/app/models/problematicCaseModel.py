from app.db import db
from app.extensions import getDatetimeNow

class ProblematicCase(db.Model):
    __tablename__ = 'problematic_case'
    id = db.Column(db.Integer(11), primary_key=True)
    registration = db.Column(db.String(40), unique=False, nullable=False)
    creation_time = db.Column(db.DateTime, default=getDatetimeNow())
    administration_edit_time = db.Column(db.DateTime, unique=False, nullable=True)
    localization = db.Column(db.String(60), unique=False, nullable=False)
    image = db.Column(db.String(120), unique=True, nullable=False)
    probability = db.Column(db.String(3), unique=False, nullable=False)
    status = db.Column(db.String(3), unique=False, nullbale=False)
    correction = db.Column(db.Boolean, unique=False, nullable=False)

    controller_number = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    admin_number = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, registration, localization, image, probability, status):
        self.registration = registration
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