from app.db import db

class Report(db.Model):
    __tablename__ = 'report'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, server_default=db.func.now())
    filename = db.Column(db.String(120), unique=False, nullable=False)
    description = db.Column(db.Text, unique=False, nullable=False) # description from when to when 
    
    def __init__(self, filename, description):
        self.filename = filename
        self.description = description
        
    def json(self):
        return {
			'id': self.id,
			'date': self.date,
			'filename': self.filename,
			'description': self.description
		}