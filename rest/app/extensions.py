import functools
from flask import g,session, redirect, url_for
import jwt
from datetime import datetime, timedelta
from config import Config
from werkzeug.security import check_password_hash

def tokenAdminRequire():
    pass

def tokenControlerRequire():
    pass

def createToken(payload, lifetime=None):
    payload['exp'] = datetime.now() + timedelta(minutes=lifetime)
    jwt_token= jwt.encode(payload, Config.SECRET_KEY, algorithm="HS256")
    refresh_payload={'session_id':session.get("session_id"),
                     'exp':datetime.now() + timedelta(days=1)
                     }
    refresh_token= jwt.encode(refresh_payload,  Config.SECRET_KEY, algorithm="HS256")
    return [jwt_token,refresh_token]

def refresh_token(jwt_token,refresh_token, lifetime=None):
    token=getDataFromToken(refresh_token)
    if token['session_id']==session.get("session_id"):
        jwt=getDataFromToken(jwt_token)
        jwt['exp']= datetime.now() + timedelta(minutes=lifetime)
        jwt_token_new= jwt.encode(jwt, Config.SECRET_KEY, algorithm="HS256")
        return [jwt_token_new,refresh_token]

def getDataFromToken(token):
    return jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])

def checkPassword(password,pwhash):
    return check_password_hash(pwhash,password)

def checkLoginData(data):
    if not checkGetData(data):
        return False
    if not "password" in data:
        return False
    return True

def checkGetData(data):
    if not "login" in data:
        return False
    return True

def checkEditData(data):
    if not checkGetData(data):
        return False
    if not "first_name" in data:
        return False
    if not "last_name" in data:
        return False
    if not "is_admin" in data:
        return False
    if not "is_controller" in data:
        return False
    return True

def checkRegistrationData(data):
    if not checkLoginData(data):
        return False
    if not "first_name" in data:
        return False
    if not "last_name" in data:
        return False
    if not "is_admin" in data:
        return False
    if not "is_controller" in data:
        return False
    return True

def toBoolean(is_boolean):
    if is_boolean in( 'true' , 'True','1'):
        return True
    if is_boolean in( 'false' , 'False','0'):
        return False
    return False


