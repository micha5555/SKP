from app.user import bp
from flask_sqlalchemy import SQLAlchemy
from flask import request,make_response
from app.models.userModel import User
from app.validators import validateLogin, validatePassword,validateName
from app.extensions import createToken,checkPassword,checkLoginData,checkRegistrationData,toBoolean,checkGetData,checkEditData
from app.db import db
import json

@bp.route('/login',methods=["POST"])
def login():
    if request.method == "POST":
        data=request.form
        if not checkLoginData(json.dumps(data)):
            return {"error":"zadanie nie zawiera wymaganych elementow"},400
        login = data["login"]
        password = data["password"]
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
        if not checkGetData(json.dumps(data)):
            return {"error":"zadanie nie zawiera wymaganych elementow"},400
        login = data["login"]
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
        data=request.form
        if not checkRegistrationData(json.dumps(data)):
            return {"error":"zadanie nie zawiera wymaganych elementow"},400
        login = data["login"]
        password = data["password"]
        if not validateLogin(login) or  not validatePassword(password):
            return {"error":"Login i hasło nie przeszły walidacji"},404
        if not validateName(data["first_name"]) or  not validateName(data["last_name"]):
            return {"error":"Imie i nazwisko nie przeszły walidacji"},404
        user = User(
            first_name=data["first_name"],
            last_name=data["last_name"],
            login=data["login"],
            password=data["password"],
            is_admin=toBoolean(data["is_admin"]),
            is_controller=toBoolean(data["is_controller"]),
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


@bp.route('/user/edit',methods=["POST"])
def edit():
       if request.method == "POST":
        data=request.form
        if not checkEditData(json.dumps(data)):
            return {"error":"zadanie nie zawiera wymaganych elementow"},400
        login = data.get("login")
        if not validateLogin(login):
            return {"error":"Login nie przeszedł walidacji"},404
        user = User.query.filter_by(login=login).first()
        if user is None:
            return {"error":"nie znaleziono uzytkownika"},404
        else: 
            user.first_name=data["first_name"]
            user.last_name=data["last_name"]
            user.password=data["password"]
            user.is_admin=toBoolean(data["is_admin"])
            user.is_controller=toBoolean(data["is_controller"])
            db.session.commit()
            return "Poprawnie zmieniono użytkownika",200


@bp.route('/user/del',methods=["POST"])
def delete():
    if request.method == "POST":
        data=request.args
        if not checkGetData(json.dumps(data)):
            return {"error":"zadanie nie zawiera wymaganych elementow"},400
        login = data.get("login")
        if not validateLogin(login):
            return {"error":"Login nie przeszedł walidacji"},404
        user = User.query.filter_by(login=login).first()
        if user is None:
            return {"error":"nie znaleziono uzytkownika"},404
        else:
            db.session.delete(user)
            db.session.commit()
            return "użytkownik usunięty poprawnie" ,200

@bp.route('/users',methods=["GET"])
def getAll():
    if request.method == "GET":
        users = db.session.query(User).all()
        users_json=[]
        if users is None:
            return {"error":"brak uzytkowników w bazie"},404
        else:
            for user in users:
                users_json.append(User.json(user))
            response_data =users_json
            response = make_response(response_data)
            response.headers['Content-Type'] = 'application/json'
            return response,200