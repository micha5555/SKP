from flask import request, make_response
from app.notPaidCase import bp
from app.extensions import *
from app.validators import *
from app.models.notPaidCaseModel import NotPaidCase
from app.db import db
from config import Config

@bp.route('/', methods=["GET"])
def get():
    if request.method == "GET":
        data = NotPaidCase.query\
            .order_by(NotPaidCase.detect_time.asc())\
            .all()
        response_data = [x.json() for x in data]
        response = make_response(response_data)
        response.headers['Content-Type'] = 'application/json'
        return response,200

@bp.route('/add', methods=["POST"])
def add():
    if request.method == "POST":
        data = getRequestData(request)
        if not allElementsInList(NotPaidCase.attr, data):
            return {"error": "request is missing"}, 400
        
        if not validateId(data['controller_id']):
            return {"error": "Controller id is incorrect"}, 400
        if not validateRegistration(data['register_plate']):
            return {"error": "Registration plate value is incorrect"}, 400
        if not validateDate(data['datetime']):
            return {"error": "Datetime value is incorrect"}, 400
        if not validateLocalization(data['location']):
            return {"error": "Location value is incorrect"}, 400
        if not validateProbability(data['probability']):
            return {"error": "Probability value is incorrect"}, 400

        registration = data['register_plate']
        creation_time = data['datetime']
        localization = data['location']
        probability = data['probability']
        controller_id = data['controller_id']

        if checkIfPaid(registration, creation_time):
            return {"success": "paid case"}, 200

        file = request.files['image']
        if file.filename == '':
            return {"error": "File is empty"}, 400


        file_name = create_image_name()
        notPaidCase = NotPaidCase(
            registration,
            creation_time,
            localization,
            file_name,
        )

        notPaidCase.controller_number = controller_id
        db.session.add(notPaidCase)
        db.session.commit()
    
        # ttt = data['image']
        # file = create_image(ttt)
        # save_image_to_local(file, file_name)
        file.save(os.path.join(os.getcwd(), Config.UPLOAD_FOLDER, file_name + '.png',))

        return {"success": "not paid case created"}, 202
    return {"error": "wrong request type"}, 404
