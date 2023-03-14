from flask import request
from app.notPaidCase import bp
from app.extensions import allElementsInList, checkIfPaid, create_image, create_image_name, save_image_to_local
from app.models.notPaidCaseModel import NotPaidCase
from app.db import db
from config import Config


@bp.route('/add')
def add():
    if request.method == "POST":
        data = request.get_json()
        if not allElementsInList(NotPaidCase.attr, data):
            return {"error": "request is missing"},400
        
        registration = data.get('registration')
        creation_time = data.get('creation_time')
        localization = data.get('localization')
        image = create_image(data.get('image'))
        probability = data.get('probability')
        controller_id = data.get('controller_id')

        # validators 

        if checkIfPaid(registration, creation_time):
            return {"success": "paid case"},200

        file_name = create_image_name()
        save_image_to_local()

        notPaidCase = NotPaidCase(
            registration,
            creation_time,
            localization,
            file_name,
            probability,
            status=Config.NOT_CHECKED
        )
        notPaidCase.controller_number = controller_id
        db.session.add(notPaidCase)
        db.session.commit()

        return {"success": "not paid case created"},202
    return {"error": "wrong request type"},404
