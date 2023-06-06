from app.db import db
from datetime import datetime

class Report(db.Model):
    __tablename__ = 'report'
    id = db.Column(db.Integer, primary_key=True)
    creation_date = db.Column(db.DateTime, server_default=db.func.now())
    start_period = db.Column(db.DateTime)
    end_period = db.Column(db.DateTime)
    filename = db.Column(db.String(120), unique=False, nullable=False)
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    attr = ["start_period", "end_period"]

    def __init__(self, start_period, end_period, filename, user_id):
        self.creation_date = datetime.now()
        self.start_period = start_period
        self.end_period = end_period
        self.filename = filename
        self.user_id = user_id
        
    def json(self):
        createion = self.creation_date.strftime('%Y-%m-%d %H:%M:%S')
        start = self.start_period.strftime('%Y-%m-%d %H:%M:%S')
        end = self.end_period.strftime('%Y-%m-%d %H:%M:%S')
        return {
			'id': self.id,
			'creation_date': createion,
            'start_period': start,
            'end_period': end,
			'filename': self.filename,
		}