from flask import request, make_response
from app.notPaidCase import bp
from app.extensions import *
from app.validators import *
from app.models.notPaidCaseModel import NotPaidCase
from app.auth import tokenUserRequire
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
@tokenUserRequire
def add(curr_user):
    data = getRequestData(request)

    if not allElementsInList(data,NotPaidCase.attr):
        return "W zapytaniu nie zawarto wszystkich wartości", 400
    
    if not validateRegistration(data['register_plate']):
        return "Błędna rejestracja", 406    
    if not validateDate(data['datetime']):
        return "Błądny format czasu", 407
    if not validateLocalization(data['location']):
        return "Błędny format lokalizacji", 408
    if not validateProbability(data['probability']):
        return "Błędny format prawdopodobieństwa", 409

    registration = data['register_plate']
    creation_time = data['datetime']
    localization = data['location']
    probability = data['probability']
    controller_id = curr_user['id']

    if checkIfPaid(registration, creation_time):
        data = {'message': 'Opłacony'}
        return makeResponse(data, 200)

    file = request.files['image']
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

    save_image_to_local(file, file_name)

    data = {"message": "Nieopłacony przypadek zapisano poprawnie"}
    return makeResponse(data, 202)
