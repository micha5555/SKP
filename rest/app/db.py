from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

def createDb():
    db.drop_all()
    from app.models.userModel import User
    from app.models.notPaidCaseModel import NotPaidCase
    from app.models.problematicCaseModel import ProblematicCase
    from app.models.reportModel import Report
    db.create_all()
    user = User("test", "test", "test", "test", True, True)
    db.session.add(user)
    db.session.commit()
    
def deleteDB():
    db.drop_all()