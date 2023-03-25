from app.user import bp
from flask import request,make_response,session
from app.models.userModel import User
from app.validators import validateLogin, validatePassword,validateName
from app.extensions import createToken,checkPassword,checkLoginData,checkAllData,toBoolean,checkGetData
from app.db import db
import json

@bp.route('/login',methods=["POST"])
def login():
    if request.method == "POST":
        data=request.form
        if not checkLoginData(json.dumps(data)):
            return {"error":"Zadanie nie zawiera wymaganych elementow"},400
        login = data["login"]
        password = data["password"]
        if not validateLogin(login) or not validatePassword(password):
            return {"error":"Login i haslo nie przeszly walidacji"},404
        user = User.query.filter_by(login=login).first()
        if user is None:
            return {"error":"Nie znaleziono uzytkownika"},404
        if(checkPassword(password,user.password)):
            session["id"]=user.id
            payload=user.generatePayload()
            auth_token=createToken(payload=payload,lifetime=60)
            response_data = {'auth_token': auth_token[0], 'refresh_token': auth_token[1]}
            response = make_response(response_data)
            response.headers['Content-Type'] = 'application/json'
            return response,200
        else:
            return {"error":"Haslo niepoprawne"},404

@bp.route('/get/<int:id>',methods=["GET"])
def get(id):
    if request.method == "GET":
        user = User.query.filter_by(id=id).first()
        if user is None:
            return {"error":"Nie znaleziono uzytkownika"},404
        else:
            response_data = user.json()
            response = make_response(response_data)
            response.headers['Content-Type'] = 'application/json'
            return response,200

@bp.route('/add' ,methods=["POST"])
def create():
    if request.method == "POST":
        data=request.form
        if not checkAllData(json.dumps(data)):
            return {"error":"Zadanie nie zawiera wymaganych elementow"},400
        login = data["login"]
        password = data["password"]
        if not validateLogin(login) or not validatePassword(password):
            return {"error":"Login i haslo nie przeszly walidacji"},404
        if not validateName(data["first_name"]) or not validateName(data["last_name"]):
            return {"error":"Imie i nazwisko nie przeszly walidacji"},404
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
            return {"error":"Login zajety"},404
        db.session.add(user)
        db.session.commit()
        payload=user.generatePayload()
        auth_token=createToken(payload=payload,lifetime=60)
        response_data = {'auth_token': auth_token[0], 'refresh_token': auth_token[1]}
        response = make_response(response_data)
        response.headers['Content-Type'] = 'application/json'
        return response,200


@bp.route('/edit',methods=["PATCH"])
def edit():
       if request.method == "PATCH":
        data=request.form
        if not checkAllData(json.dumps(data)):
            return {"error":"Zadanie nie zawiera wymaganych elementow"},400
        login = data.get("login")
        if not validateLogin(login) or not validatePassword(data["password"]):
            return {"error":"Login i haslo nie przeszly walidacji"},404
        if not validateName(data["first_name"]) or not validateName(data["last_name"]):
            return {"error":"Imie i nazwisko nie przeszly walidacji"},404
        user = User.query.filter_by(login=login).first()
        if user is None:
            return {"error":"Nie znaleziono uzytkownika"},404
        else: 
            user.first_name=data["first_name"]
            user.last_name=data["last_name"]
            user.password=data["password"]
            user.is_admin=toBoolean(data["is_admin"])
            user.is_controller=toBoolean(data["is_controller"])
            db.session.commit()
            return {"message":"Poprawnie zmieniono użytkownika"},200


@bp.route('/del',methods=["DELETE"])
def delete():
    if request.method == "DELETE":
        data=request.form
        if not checkGetData(json.dumps(data)):
            return {"error":"Zadanie nie zawiera wymaganych elementow"},400
        login = data.get("login")
        if not validateLogin(login):
            return {"error":"Login nie przeszedł walidacji"},404
        user = User.query.filter_by(login=login).first()
        if user is None:
            return {"error":"Nie znaleziono uzytkownika"},404
        else:
            db.session.delete(user)
            db.session.commit()
            return {"message":"Uzytkownik usuniety poprawnie"} ,200

@bp.route('/users',methods=["GET"])
def getAll():
    if request.method == "GET":
        users =  User.query.all()
        users_json=[]
        if users is None:
            return {"error":"Brak uzytkowników w bazie"},404
        else:
            for user in users:
                users_json.append(user.json())
            response_data =users_json
            response = make_response(response_data)
            response.headers['Content-Type'] = 'application/json'
            return response,200