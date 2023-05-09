from app.user import bp
from flask import request,make_response,session
from app.models.userModel import User
from app.validators import validateLogin, validatePassword,validateName
from app.extensions import createToken,checkPassword,checkLoginData,checkAllData,toBoolean,allElementsInList
from app.db import db
import json

@bp.route('/login',methods=["POST"])
def login():
    if request.method == "POST":
        data=request.get_json()
        if not allElementsInList(data,User.loginAttr):
            return {"error":"Request dont have all elements"},400
        if not validateLogin(data["login"]) or not validatePassword(data["password"]):
            return {"error":"Login or password is not safe"},404
        login = data["login"]
        user = User.query.filter_by(login=login).first()
        if user is None:
            return {"error":"User not found"},404
        if(checkPassword(password,user.password)):
            session["id"]=user.id
            payload=user.generatePayload()
            auth_token=createToken(payload=payload,lifetime=60)
            response_data = {'auth_token': auth_token[0], 'refresh_token': auth_token[1]}
            response = make_response(response_data)
            response.headers['Content-Type'] = 'application/json'
            return response,200
        else:
            return {"error":"Incorrect password"},404

@bp.route('/get/<int:id>',methods=["GET"])
def get(id:int):
    if request.method == "GET":
        user = User.query.filter_by(id=id).first()
        if user is None:
            return {"error":"User not found"},404
        else:
            response_data = user.json()
            response = make_response(response_data)
            response.headers['Content-Type'] = 'application/json'
            return response,200

@bp.route('/add' ,methods=["POST"])
def create():
    if request.method == "POST":
        data=request.get_json()
        if not allElementsInList(data,User.attr):
            return {"error":"Request dont have all elements"},400
        if not validateLogin(data["login"]) or not validatePassword(data["password"]):
            return {"error":"Login or password is not safe"},404
        if not validateName(data["first_name"]) or not validateName(data["last_name"]):
            return {"error":"Firstname or surname is not correct"},404
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
            return {"error":"Login already exist"},404
        db.session.add(user)
        db.session.commit()
        payload=user.generatePayload()
        auth_token=createToken(payload=payload,lifetime=60)
        response_data = {'auth_token': auth_token[0], 'refresh_token': auth_token[1]}
        response = make_response(response_data)
        response.headers['Content-Type'] = 'application/json'
        return response,200


@bp.route('/edit/<int:id>',methods=["PUT"])
def edit(id:int):
       if request.method == "PUT":
        data=request.get_json()
        if not allElementsInList(data,User.attr):
            return {"error":"Request dont have all elements"},400
        if not validateName(data["first_name"]) or not validateName(data["last_name"]):
            return {"error":"Firstname or surname is not correct"},404
        if not validatePassword(data["password"]):
            return {"error":"New password is not safe"},404
        else: 
            user = User.query.filter_by(id=id).first()
            user.first_name=data["first_name"]
            user.last_name=data["last_name"]
            user.password=data["password"]
            user.is_admin=toBoolean(data["is_admin"])
            user.is_controller=toBoolean(data["is_controller"])
            db.session.commit()
            return {"message":"User changed correctly"},200


@bp.route('/del/<int:id>',methods=["DELETE"])
def delete(id:int):
    if request.method == "DELETE":
        user = User.query.filter_by(id=id).first()
        if user is None:
            return {"error":"User not found"},404
        else:
            db.session.delete(user)
            db.session.commit()
            return {"message":"User removed"} ,200

@bp.route('/users',methods=["GET"])
def getAll():
    if request.method == "GET":
        users =  User.query.all()
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