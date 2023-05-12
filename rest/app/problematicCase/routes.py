from flask import request, make_response
from app.problematicCase import bp
from app.db import db
from app.models.problematicCaseModel import ProblematicCase
from app.extensions import *
from app.validators import *
from config import Config

@bp.route('/', methods=["GET"])
def get():
    if request.method == "GET":
        data = ProblematicCase.query\
            .filter_by(status=Config.NOT_CHECKED)\
            .order_by(ProblematicCase.detect_time.asc())\
            .all()
        resonse_data = [x.json() for x in data]
        response = make_response(resonse_data)
        response.headers['Content-Type'] = 'application/json'
        return response, 200

@bp.route('/id>', methods=["GET"])
def get_id(id):
    if request.method == "GET":
        if not validateId(id):
            return {"error": "Id is not numeric"}, 400

        return ProblematicCase.query\
            .filter(ProblematicCase.id==id)\
            .filter(ProblematicCase.status==Config.NOT_CHECKED)\
            .order_by(ProblematicCase.detect_time.asc())\
            .first().json()

@bp.route('/add', methods=["POST"])
def add():
    if request.method == "POST":
        data = getRequestData()

        if not allElementsInList(ProblematicCase.attr, data):
            return {"error": "request is missing"}, 400
        
        if not validateRegistration(data['register_plate']):
            return{"error":"Wrong registration"}, 406
        if not validateDate(data['datetime']):
            return{"error":"Wrong creation time"}, 406
        if not validateLocalization(data['location']):
            return{"error":"Wrong creation time"}, 406
        if not validateProbability(data['probability']):
            return{"error":"Wrong probability"}, 406
        if not validateId(data['controller_id']):
            return{"error":"Wrong id"}, 406
        
        registration = data['register_plate']
        creation_time = data['datetime']
        localization = data['location']
        probability = data['probability']
        controller_id = data['controller_id']

        file = request.files['image']
        if file.filename == '':
            return {"error": "File is empty"}, 400
        
        file_name = create_image_name()
        newProblematicCase = ProblematicCase(
            registration,
            creation_time,
            localization,
            file_name,
            probability,
            status=Config.NOT_CHECKED
        )
        newProblematicCase.controller_number = controller_id
        db.session.add(newProblematicCase)
        db.session.commit()
        file.save(os.path.join(
            os.getcwd(), 
            Config.UPLOAD_FOLDER, 
            file_name + '.png',
        ))

        return {"message": "saved problematic case succesfully"},202
    return {"error": "wrong request type"},404

@bp.route('/edit/<id>', methods=["PUT"])
def edit(id):
    if request.method == "PUT":
        data = getRequestData()

        if not allElementsInList(ProblematicCase.attr_edit, data):
            return {"error": "request is missing"}, 400

        if not validateRegistration(data['registration']):
            return{"error":"Wrong registration"}, 406
        if not validateDate(data['administration_edit_time']):
            return{"error":"Wrong administration edit time"}, 406
        if not validateId(id):
            return{"error":"Wrong id"}, 406

        registration = data['registration']
        administration_edit_time = data['administration_edit_time']

        problematicCase = ProblematicCase.query.filter_by(id=id).first()
        if problematicCase:
            problematicCase.registration = registration
            problematicCase.administration_edit_time = administration_edit_time
            db.session.commit()

            return {'message': 'saved problematic case sucessfully'},200
        return {"error": "problematic case with given id not exist"},404
    return {"error": "wrong request type"},404

#TODO sposób przekazywania statusu - jeszcze nie wiem jak dokładnie będzie
@bp.route('/correction/<id>', methods=["PUT"])
def correctToNotPaid(id):
    if request.method == "PUT":
        data = getRequestData()

        if not allElementsInList(ProblematicCase.attr_change, data):
            return {"error": "request is missing"},400
        
        # if not validateStatus(status):
        #    return{"error":"Wrong status"},406
        if not validateId(id):
            return{"error":"Wrong id"},406
        # if not validateId(admin_id):
            # return{"error":"Wrong admin id"},406
        
        status = data['status']

        problematicCase = ProblematicCase.query.filter_by(id=id).first()
        if not problematicCase:
            return {"error": "problematic case with given id not exist"},404

        # from require token
        problematicCase.admin_number = 1
        problematicCase.correction = True

        if status == 'not_possible_to_check':
            problematicCase.status = Config.CHECKED_NOT_CONFIRMED
        elif status == 'check_if_paid_again':
            if(not checkIfPaid()):
                problematicCase.status = Config.CHECKED_TO_PAID
            else:
                problematicCase.status = Config.CHECKED_OK
            return {'message': 'saved problematic case sucessfully'},200
        return {"error": "wrong status type"},404
    return {"error": "wrong request type"},404