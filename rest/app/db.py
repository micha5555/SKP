from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

def createDb():
    db.drop_all()
    db.create_all() 
    
def deleteDB():
    db.drop_all()