from flask import request, session
from app.user import bp
from app.models.userModel import User
from app.validators import *
from app.extensions import *
from app.auth import *
from app.db import db

@bp.route('/login', methods=["POST"])
def login():
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
        session["user_id"] = user.id
        payload = user.generatePayload()
        auth_token = createToken(payload=payload, lifetime=60)
        response_data = {'auth_token': auth_token[0], 'refresh_token': auth_token[1]}
        return makeResponse(response_data, 200)
    return "Incorrect password", 401

@bp.route('/user', methods=["GET"])
@tokenAdminRequire
def getAll(curr_user):
    users = User.query.all()
    users_json=[]

    if users is None:
        return "W bazie nie ma użytkowników", 404
    
    for user in users:
        users_json.append(user.json())
    response_data = users_json
    return makeResponse(response_data, 200)

@bp.route('/user/<id>', methods=["GET"])
@tokenAdminRequire
def get(curr_user, id):
    if not validateId(id):
        return "Podane id nie jest wartością numeryczną", 404

    user = User.query.filter_by(id=id).first()
    if user is None:
        return "Użytkownik o podanym id nie istnieje", 404

    response_data = user.json()
    return makeResponse(response_data, 200)

@bp.route('/user/add', methods=["POST"])
@tokenAdminRequire
def create(curr_user):
    data = getRequestData(request)
    
    if not allElementsInList(data, User.attr):
        return "Podane id nie jest wartością numeryczną", 404
    if not validateLogin(data["login"]):
        return "Podany login jest zbyt słaby", 404 
    if not validatePassword(data["password"]):
        return "Podane hasło jest za słabe", 404
    if not validateName(data["first_name"]):
        return "Imię zawiera niedozwolone znaki", 404
    if not validateName(data["last_name"]):
        return "Nazwisko zawiera niedozwolone znaki", 404
    if not validateBoolean(data["is_admin"]) or not validateBoolean(data["is_controller"]):
        return "Admin i kotroler przyjmują wartość true/false", 404
    
    checkUserExistence = User.query.filter_by(login=data['login']).first()
    if checkUserExistence is not None:
        return "Podany login jest już zajęty", 409
    
    user = User(
        first_name = data["first_name"],
        last_name = data["last_name"],
        login = data["login"],
        password = data["password"],
        is_admin = toBoolean(data["is_admin"]),
        is_controller = toBoolean(data["is_controller"]),
    )
    
    db.session.add(user)
    db.session.commit()
    data = {'message': "Użytkownik został utworzony pomyślnie."}
    return makeResponse(data, 202)

@bp.route('/user/edit/<id>', methods=["PUT"])
@tokenAdminRequire
def edit(curr_user, id):
    data = getRequestData(request)
    if not validateId(id):
        return "Podane id nie jest wartością numeryczną", 404
    if not allElementsInList(data, User.attr_edit):
        return "Zapytanie nie zawiera wszystkich elementów", 404
    if not validateLogin(data["login"]):
        return "Podany login jest zbyt słaby", 404 
    if not validateName(data["first_name"]):
        return "Imię zawiera niedozwolone znaki", 404
    if not validateName(data["last_name"]):
        return "Nazwisko zawiera niedozwolone znaki", 404
    if not validateBoolean(data["is_admin"]) or not validateBoolean(data["is_controller"]):
        return "Admin i kotroler przyjmują wartość true/false", 404
    
    user = User.query.filter_by(id=id).first()
    if user is None:
        return "Użytkownik nie istnieje", 404
    
    user.first_name = data["first_name"]
    user.last_name = data["last_name"]
    user.is_admin = toBoolean(data["is_admin"])
    user.is_controller = toBoolean(data["is_controller"])
    
    db.session.commit()
    data = {"message":"Użytkownik został zapisany."}
    return makeResponse(data, 201)


@bp.route('/user/del/<id>', methods=["DELETE"])
@tokenAdminRequire
def delete(curr_user, id):
    if not validateId(id):
        return "Podane id nie jest wartością numeryczną", 404
    
    user = User.query.filter_by(id=id).first()
    if user is None:
        return "Użytkownik o podanym id nie istnieje", 404
    
    db.session.delete(user)
    db.session.commit()
    data = {"message":"Użytkownik został usunięty."}
    return makeResponse(data, 200)