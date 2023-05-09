from flask_sqlalchemy import SQLAlchemy
from config import Config
import os
db = SQLAlchemy()

def createDb():
    from app.models.notPaidCaseModel import NotPaidCase
    from app.models.problematicCaseModel import ProblematicCase
    from app.models.reportModel import Report
    from app.models.userModel import User
    db.drop_all()
    folder = Config.UPLOAD_FOLDER
    file_list = os.listdir(folder)
    for file_name in file_list:
        file_path = os.path.join(folder, file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)
    db.create_all() 
    user = User("test", "test", "test", "test", True, True)
    db.session.add(user)
    db.session.commit()
    
def deleteDB():
    from app.models.userModel import User
    from app.models.notPaidCaseModel import NotPaidCase
    from app.models.problematicCaseModel import ProblematicCase
    from app.models.reportModel import Report

    folder = Config.UPLOAD_FOLDER
    file_list = os.listdir(folder)
    for file_name in file_list:
        file_path = os.path.join(folder, file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)

    db.drop_all()