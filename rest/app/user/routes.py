from app.user import bp
from flask import request,make_response,session
from app.models.userModel import User
from app.validators import *
from app.extensions import *
from app.db import db
import json

@bp.route('/login', methods=["POST"])
def login():
    if request.method == "POST":
        data = getRequestData(request)

        if not allElementsInList(data, User.loginAttr):
            return "Request dont have all elements", 400
        if not validateLogin(data["login"]) or not validatePassword(data["password"]):
            return "Login or password is not safe", 404

        login = data["login"]
        password = data['password']

        user = User.query.filter_by(login=login).first()
        if user is None:
            return "User not found", 404
        
        if(checkPassword(password, user.password)):
            session["id"]=user.id
            payload = user.generatePayload()
            auth_token = createToken(payload=payload, lifetime=60)
            response_data = {'auth_token': auth_token[0], 'refresh_token': auth_token[1]}
            response = make_response(response_data)
            response.headers['Content-Type'] = 'application/json'
            return response,200
        else:
            return "Incorrect password", 401

@bp.route('/user', methods=["GET"])
def getAll():
    if request.method == "GET":
        users = User.query.all()
        users_json=[]
        if users is None:
            return {"error":"No user in DB"},404
        else:
            for user in users:
                users_json.append(user.json())
            response_data =users_json
            response = make_response(response_data)
            response.headers['Content-Type'] = 'application/json'
            return response,200 

@bp.route('/user/<id>', methods=["GET"])
def get(id):
    if request.method == "GET":
        if not validateId(id):
            return {"error":"Id must be instance od integer"}, 404

        user = User.query.filter_by(id=id).first()
        if user is None:
            return {"error":"User not found"}, 404
        else:
            for user in users:
                users_json.append(user.json())
            response_data =users_json
            response = make_response(response_data)
            response.headers['Content-Type'] = 'application/json'
            return response, 200

@bp.route('/user/add', methods=["POST"])
def create():
    if request.method == "POST":
        data = getRequestData(request)
        
        if not allElementsInList(data, User.attr):
            return {"error":"Request dont have all elements"}, 400
        if not validateLogin(data["login"]) or not validatePassword(data["password"]):
            return {"error":"Login or password is not safe"}, 404
        if not validateName(data["first_name"]) or not validateName(data["last_name"]):
            return {"error":"Firstname or surname is not correct"}, 404
        if not validateBoolean(data["is_admin"]) or not validateBoolean(data["is_controller"]):
            return {"error":"Boolean is not correct"}, 404
        
        checkUserExistence = User.query.filter_by(login=data['login']).first()
        if checkUserExistence is not None:
            return {"error":"Login already exist"}, 409
        
        user = User(
            first_name = data["first_name"],
            last_name = data["last_name"],
            login = data["login"],
            password = data["password"],
            # Czy walidacja do boolean nie powinna być w wyżej a nie tu?        
            is_admin = toBoolean(data["is_admin"]),
            is_controller = toBoolean(data["is_controller"]),
        )
        
        db.session.add(user)
        db.session.commit()
        return {'message': "User created successfully"}, 200

@bp.route('/user/edit/<id>', methods=["PUT"])
def edit(id):
    if request.method == "PUT":
        data = getRequestData(request)

        if not validateId(id):
            return {"error":"Id must be instance od integer"}, 404
        if not allElementsInList(data, User.attr_edit):
            return {"error":"Request don't have all elements"}, 400
        if not validateName(data["first_name"]) or not validateName(data["last_name"]):
            return {"error":"Firstname or surname is not correct"}, 404
        if not validateLogin(data['login']):
            return {"error":"Login is incorrect"}, 404
        if not validateBoolean(data["is_admin"]) or not validateBoolean(data["is_controller"]):
            return {"error":"Boolean is not correct"}, 404
        
        user = User.query.filter_by(id=id).first()
        user.first_name = data["first_name"]
        user.last_name = data["last_name"]
        user.is_admin = toBoolean(data["is_admin"])
        user.is_controller = toBoolean(data["is_controller"])
        db.session.commit()
        return {"message":"User changed successfully"}, 200


@bp.route('/user/del/<id>', methods=["DELETE"])
def delete(id):
    if request.method == "DELETE":
        if not validateId(id):
            return {"error":"Id must be instance od integer"}, 404
        
        user = User.query.filter_by(id=id).first()
        if user is None:
            return {"error":"User not found"}, 404
        else:
            db.session.delete(user)
            db.session.commit()
            return {"message":"User removed"}, 200