from app.user import bp
from flask_sqlalchemy import SQLAlchemy
from flask import redirect, render_template, request, url_for
from app.models.userModel import User
from datetime import datetime
from app.validators import validateLogin, validatePassword
from app.user.auth import generate_jwt
import bcrypt

db = SQLAlchemy()

@bp.route('/login',methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return "Tamplatka"
    if request.method == "POST":
        login = request.form["login"]
        password = request.form["password"]
    if not (validateLogin(login) or validatePassword(password)):
        return {"error":"Login i hasło nie przeszły walidacji"},404
    user = User.query.filter_by(login=login).first()
    if user is None:
            return {"error":"nie znaleziono uzytkownika"},404
    if(bcrypt.using(rounds=10).verify(password,user.password)):
        payload = {
            'login': user.login,
            'id': user.id,
            'is_admin': user.is_admin,
            'is_controller': user.is_controller,
            'current_time': datetime.now()
         }
        auth_token=generate_jwt(payload=payload,lifetime=60)
        return {"access_token": auth_token[0],"refresh_token":auth_token[1]}, 200

@bp.route('/user/get')
def get():
    pass


@bp.route('/user/add' ,methods=["GET", "POST"])
def create():
    if request.method == "GET":
        return "Tamplatka"
    if request.method == "POST":
        login = request.form["login"]
        password = request.form["password"]
        if not (validateLogin(login) or validatePassword(password)):
            return {"error":"Login i hasło nie przeszły walidacji"},404
        user = User(
            first_name=request.form["first_name"],
            last_name=request.form["last_name"],
            login=request.form["login"],
            password=bcrypt.using(rounds=10).hash(password),
            is_admin=request.form["is_admin"],
            is_controller=request.form["is_controller"],
        )
        newUser = User.query.filter_by(login=login).first()
        if newUser is not None:
            return {"error":"login zajęty"},404
        db.session.add(user)
        db.session.commit()
        payload = {
            'login': user.login,
            'id': user.id,
            'is_admin': user.is_admin,
            'is_controller': user.is_controller,
            'current_time': datetime.now()
        }
        auth_token=generate_jwt(payload=payload,lifetime=60)
        return {"access_token": auth_token[0],"refresh_token":auth_token[1]}, 200


@bp.route('/user/edit')
def edit():
    pass


@bp.route('/user/del')
def delete():
    pass
