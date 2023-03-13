from app.user import bp
from flask_sqlalchemy import SQLAlchemy
from flask import request,make_response
from app.models.userModel import User
from app.validators import validateLogin, validatePassword
from app.extensions import createToken,checkPassword,checkLoginData,checkRegistrationData,toBoolean,checkGetData
from app.db import db

@bp.route('/login',methods=["POST"])
def login():
    if request.method == "POST":
        data=request.args
        if not checkLoginData(data):
            return {"error":"zadanie nie zawiera wymaganych elementow"},400
        login = data.get("login")
        password = data.get("password")
        if not validateLogin(login) or not validatePassword(password):
            return {"error":"Login i hasło nie przeszły walidacji"},404
        user = User.query.filter_by(login=login).first()
        if user is None:
            return {"error":"nie znaleziono uzytkownika"},404
        if(checkPassword(password,user.password)):
            payload=User.generatePayload(user)
            auth_token=createToken(payload=payload,lifetime=60)
            response_data = {'auth_token': auth_token[0], 'refresh_token': auth_token[1]}
            response = make_response(response_data)
            response.headers['Content-Type'] = 'application/json'
            return response,200
        else:
            return {"error":"Haslo niepoprawne"},404

@bp.route('/user/get',methods=["GET"])
def get():
    if request.method == "GET":
        data=request.args
        if not checkGetData(data):
            return {"error":"zadanie nie zawiera wymaganych elementow"},400
        login = data.get("login")
        if not validateLogin(login):
            return {"error":"Login nie przeszedł walidacji"},404
        user = User.query.filter_by(login=login).first()
        if user is None:
            return {"error":"nie znaleziono uzytkownika"},404
        else:
            response_data = User.json(user)
            response = make_response(response_data)
            response.headers['Content-Type'] = 'application/json'
            return response,200

@bp.route('/user/add' ,methods=["POST"])
def create():
    if request.method == "POST":
        data=request.args
        if not checkRegistrationData(data):
            return {"error":"zadanie nie zawiera wymaganych elementow"},400
        login = data.get("login")
        password = data.get("password")
        if not validateLogin(login) or  not validatePassword(password):
            return {"error":"Login i hasło nie przeszły walidacji"},404
        user = User(
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            login=data.get("login"),
            password=data.get("password"),
            is_admin=toBoolean(data.get("is_admin")),
            is_controller=toBoolean(data.get("is_controller")),
        )
        checkUserExistence = User.query.filter_by(login=login).first()
        if checkUserExistence is not None:
            return {"error":"login zajęty"},404
        db.session.add(user)
        db.session.commit()
        payload=User.generatePayload(user)
        auth_token=createToken(payload=payload,lifetime=60)
        response_data = {'auth_token': auth_token[0], 'refresh_token': auth_token[1]}
        response = make_response(response_data)
        response.headers['Content-Type'] = 'application/json'
        return response,200


@bp.route('/user/edit')
def edit():
    pass


@bp.route('/user/del')
def delete():
    pass
