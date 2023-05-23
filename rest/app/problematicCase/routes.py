from flask import request, make_response, send_from_directory
from app.problematicCase import bp
from app.db import db
from app.models.problematicCaseModel import ProblematicCase
from app.extensions import *
from app.validators import *
from sqlalchemy import or_
from config import Config

@bp.route('/', methods=["GET"])
def get():
    if request.method == "GET":
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 15, type=int)
        query = ProblematicCase.query

        print(request.args)

        filter_param = request.args.get('filter')
        if filter_param:
            filters = filter_param.split(',')
            filter_clauses = []
            for f in filters:
                field, value = f.split(':')
                if field == 'register':
                    filter_clauses.append(ProblematicCase.registration_plate.ilike(f'%{value}%'))
                if field == 'id':
                    filter_clauses.append(ProblematicCase.id.ilike(f'%{value}%'))
                if field == 'creation_time':
                    filter_clauses.append(ProblematicCase.detect_time.ilike(f'%{value}%'))
                if field == 'probability':
                    filter_clauses.append(ProblematicCase.probability.ilike(f'%{value}%'))

            if filter_clauses:
                query = query.filter(or_(*filter_clauses))
                

        sort_by = request.args.get('sort_by')
        order = request.args.get('order')
        if sort_by == 'creation_time':
            query = query.order_by(ProblematicCase.detect_time.desc()) if order == 'desc' else query.order_by(ProblematicCase.detect_time.asc())
        elif sort_by == 'probability':
            query = query.order_by(ProblematicCase.probability.desc())

        problematic_cases = query.paginate(page=page, per_page=per_page)
        resonse_data = [case.json() for case in problematic_cases]

        response = make_response(resonse_data)
        response.headers['Content-Type'] = 'application/json'
        return response, 200

@bp.route('/<id>', methods=["GET"])
def get_id(id):
    if request.method == "GET":
        if not validateId(id):
            return {"error": "Id is not numeric"}, 400

        return ProblematicCase.query\
            .filter(ProblematicCase.id==id)\
            .filter(ProblematicCase.status==Config.NOT_CHECKED)\
            .order_by(ProblematicCase.detect_time.asc())\
            .first().json()

@bp.route('/images/<filename>', methods=["GET"])
def get_image(filename):
    image_folder = Config.UPLOAD_FOLDER 

    print(os.path.join(os.getcwd(), image_folder, filename + '.png'))
    if not os.path.isfile(os.path.join(os.getcwd(), image_folder, filename + '.png')):
        return {"error": "Image not found"}, 404
    
    return send_from_directory(os.path.join(os.getcwd(), image_folder), filename + ".png")

@bp.route('/add', methods=["POST"])
def add():
    if request.method == "POST":
        data = getRequestData(request)

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

        # ttt = data['image']
        # file = create_image(ttt)
        # save_image_to_local(file, file_name)
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
        data = getRequestData(request)

        if not allElementsInList(ProblematicCase.attr_edit, data):
            return {"error": "request is missing"}, 400

        if not validateRegistration(data['registration']):
            return{"error":"Wrong registration"}, 406
        if not validateId(id):
            return{"error":"Wrong id"}, 406
        
        registration = data['registration']
        status = data['status']

        problematicCase = ProblematicCase.query.filter_by(id=id).first()
        if problematicCase:
            problematicCase.registration = registration
            problematicCase.administration_edit_time = datetime.now()
            problematicCase.correction = True
            ### 
            # data from token
            problematicCase.admin_number = 2
            ###
            if status == 'not_possible_to_check':
                problematicCase.status = Config.CHECKED_NOT_CONFIRMED
            elif status == 'check_if_paid_again':
                if(not checkIfPaid(problematicCase.registration_plate, problematicCase.detect_time)):
                    problematicCase.status = Config.CHECKED_TO_PAID
                else:
                    problematicCase.status = Config.CHECKED_OK
            db.session.commit()

            return {'message': 'saved problematic case sucessfully'},200
        return {"error": "problematic case with given id not exist"},404
    return {"error": "wrong request type"},404