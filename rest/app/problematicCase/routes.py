import uuid
import os
import base64
from datetime import datetime
from io import BytesIO
from PIL import Image
from flask import request
from app.problematicCase import bp
from app.db import db
from app.models.problematicCaseModel import ProblematicCase
from app.extensions import allElementsInList
from config import Config

@bp.route('/', methods=["GET"])
def get():
    if request.method == "GET":
        return ProblematicCase.query\
            .filter_by(status=Config.NOT_CHECKED)\
            .order_by(ProblematicCase.creation_time.asc())\
            .all()

@bp.route('/<id>', methods=["GET"])
def get_id(id_p):
    if request.method == "GET":

        # validator missing
        
        return ProblematicCase.query\
            .filter(id=id_p)\
            .filter(status=Config.NOT_CHECKED)\
            .order_by(ProblematicCase.creation_time.asc())\
            .first()

@bp.route('/add', methods=["POST"])
def add():
    if request.method == "POST":
        data = request.get_json()
        if not allElementsInList(ProblematicCase.attr, data):
            return {"error": "request is missing"},400
        
        registration = data.get('registration')
        creation_time = data.get('creation_time')
        localization = data.get('localization')
        image = base64.b64decode(data.get('image'))
        probability = data.get('probability')
        
        # This will be taken from token
        # controller_id = 

        # validators 

        file_uuid = uuid.uuid4()
        now = datetime.now()
        file_name = f"{file_uuid}_{now.strftime('%Y5m%d_%H%M%S')}"

        with BytesIO(image) as f:
            save_image = Image.open(f)
            save_image.save(os.path.join(os.getcwd(), Config.UPLOAD_FOLDER, file_name), format="PNG")

        if image:
            newProblematicCase = ProblematicCase(
                registration,
                creation_time,
                localization,
                file_name,
                probability,
                status=Config.NOT_CHECKED
            )
            # newProblematicCase.controller_number = controller_id
            newProblematicCase.controller_number = 1
            db.session.add(newProblematicCase)
            db.session.commit()

            return {"message": "saved problematic case succesfully"},202
        return {"error": "wrong image"},400
    return {"error": "wrong request type"},404

@bp.route('/edit', methods=["PUT"])
def edit():
    if request.method == "PUT":
        if not allElementsInList(ProblematicCase.attr_edit, request.form):
            return {"error": "request is missing"},400
        id = request.form['id']
        registration = request.form['registration']
        administration_edit_time = request.form['administration_edit_time']
        admin_id = request.form['admin_id']

        # validators 

        problematicCase = ProblematicCase.query.filter_by(id=id).first()
        if problematicCase:
            problematicCase.registration = registration
            problematicCase.administration_edit_time = administration_edit_time
            problematicCase.admin_id = admin_id
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

        # validators 

        problematicCase = ProblematicCase.query.filter_by(id=id).first()
        if problematicCase:
            problematicCase.status = status
            db.session.commit()

            return {'message': 'saved problematic case sucessfully'},200
        return {"error": "problematic case with given id not exist"},404
    return {"error": "wrong request type"},404