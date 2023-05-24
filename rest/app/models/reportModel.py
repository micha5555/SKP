from app.db import db
from datetime import datetime

class Report(db.Model):
    __tablename__ = 'report'
    id = db.Column(db.Integer, primary_key=True)
    creation_date = db.Column(db.DateTime, server_default=db.func.now())
    start_period = db.Column(db.DateTime)
    end_period = db.Column(db.DateTime)
    filename = db.Column(db.String(120), unique=False, nullable=False)
    
    attr = ["start_period", "end_period"]

    def __init__(self, start_period, end_period, filename):
        self.creation_date = datetime.now()
        self.start_period = start_period
        self.end_period = end_period
        self.filename = filename
        
    def json(self):
        return {
			'id': self.id,
			'creation_date': self.creation_date,
            'start_period': self.start_period,
            'end_period': self.end_period,
			'filename': self.filename,
		}