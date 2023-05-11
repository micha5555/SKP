from flask import request
from app.problematicCase import bp
from app.db import db
from app.models.problematicCaseModel import ProblematicCase
from app.extensions import \
    allElementsInList,\
    create_image,\
    create_image_name,\
    save_image_to_local,\
    checkIfPaid
from config import Config
from app.validators import validateId,validateDate,validateLocalization

@bp.route('/', methods=["GET"])
def get():
    if request.method == "GET":
        return ProblematicCase.query\
            .filter_by(status=Config.NOT_CHECKED)\
            .order_by(ProblematicCase.detect_time.asc())\
            .all()

@bp.route('/<int:id_p>', methods=["GET"])
def get_id(id_p):
    if request.method == "GET":
        return ProblematicCase.query\
            .filter(ProblematicCase.id==id_p)\
            .filter(ProblematicCase.status==Config.NOT_CHECKED)\
            .order_by(ProblematicCase.detect_time.asc())\
            .first().json()

@bp.route('/add', methods=["POST"])
def add():
    if request.method == "POST":
        data = request.get_json()
        if not allElementsInList(ProblematicCase.attr, data):
            return {"error": "request is missing"},400
        
        registration = data.get('register_plate')
        creation_time = data.get('datetime')
        localization = data.get('location')
        image = create_image(data.get('image'))
        probability = data.get('probability')
        controller_id = data.get('controller_id')

        # validators 
        if not validateRegistration(registration):
            return{"error":"Wrong registration"},406
        if not validateDate(creation_time):
            return{"error":"Wrong creation time"},406
        if not validateLocalization(localization):
            return{"error":"Wrong creation time"},406
        if not validateProbability(probability):
            return{"error":"Wrong probability"},406
        if not validateId(controller_id):
            return{"error":"Wrong id"},406
        
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
        save_image_to_local(image, file_name + '.png')

        return {"message": "saved problematic case succesfully"},202
    return {"error": "wrong request type"},404

@bp.route('/edit', methods=["PUT"])
def edit():
    if request.method == "PUT":
        if not allElementsInList(ProblematicCase.attr_edit, request.form):
            return {"error": "request is missing"},400
        id = request.form['id']
        registration = request.form['registration']
        administration_edit_time = request.form['administration_edit_time']

        if not validateRegistration(registration):
            return{"error":"Wrong registration"},406
        if not validateDate(administration_edit_time):
            return{"error":"Wrong administration edit time"},406
        if not validateId(id):
            return{"error":"Wrong id"},406

        problematicCase = ProblematicCase.query.filter_by(id=id).first()
        if problematicCase:
            problematicCase.registration = registration
            problematicCase.administration_edit_time = administration_edit_time
            db.session.commit()

            return {'message': 'saved problematic case sucessfully'},200
        return {"error": "problematic case with given id not exist"},404
    return {"error": "wrong request type"},404

@bp.route('/correction', methods=["PUT"])
def correctToNotPaid():
    if request.method == "PUT":
        if not allElementsInList(ProblematicCase.attr_change, request.form):
            return {"error": "request is missing"},400
        id = request.form['id']
        status = request.form['status']
        admin_id = request.form['admin_id']
        #TODO
        #if not validateStatus(status):
           # return{"error":"Wrong status"},406
        if not validateId(id):
            return{"error":"Wrong id"},406
        if not validateId(admin_id):
            return{"error":"Wrong admin id"},406
        
        problematicCase = ProblematicCase.query.filter_by(id=id).first()
        if not problematicCase:
            return {"error": "problematic case with given id not exist"},404

        problematicCase.admin_number = admin_id
        problematicCase.correction = True
        if status == 'not_possible_to_check':
            problematicCase.status = Config.CHECKED_NOT_CONFIRMED
        elif status == 'check_if_paid_again':
            if(not checkIfPaid()):
                problematicCase.status = Config.CHECKED_TO_PAID
            else:
                problematicCase.status = Config.CHECKED_OK
            return {'message': 'saved problematic case sucessfully'},200
        else:
            return {"error": "wrong status type"},404
        return {"error": "wrong request"},404    
    return {"error": "wrong request type"},404