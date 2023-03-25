import os
import jwt
import uuid
import base64
import datetime
import requests
import functools
from flask import g,session
from datetime import datetime, timezone, timedelta
from PIL import Image
from io import BytesIO
from werkzeug.security import check_password_hash
from config import Config

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
    if "login" not in data:
        return False
    if "password" not in data:
        return False
    return True

def checkGetData(data):
    if "login" not in data:
        return False
    return True

def checkAllData(data):
    if not checkLoginData(data):
        return False
    if "first_name" not in data:
        return False
    if "last_name" not in data:
        return False
    if  "is_admin" not in data:
        return False
    if "is_controller" not in data:
        return False
    return True

def toBoolean(is_boolean):
    if is_boolean.lower() in( 'true' ,'1'):
        return True
    if is_boolean.lower() in( 'false','0'):
        return False
    return False

# We get time from UTC,, but we need Poland time zone so we need to add +1 to hour
def createDatetime(string):
    dt_utc = datetime.strptime(string, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone.utc)
    dt_local = dt_utc.astimezone(timezone(timedelta(hours=1)))
    return dt_local

# We get current time from UTC,, but we need Poland time zone so we need to add +1 to hour
def getDatetimeNow():
    dt_utc = datetime.utcnow().replace(tzinfo=timezone.utc)
    dt_local = dt_utc.astimezone(timezone(timedelta(hours=1)))
    return dt_local

def allElementsInList(elements, lst):
    return all(element in lst for element in elements)

def checkIfPaid(registration, detection_time):
    # here will be created element which will check if element was paid or not 
    payload = {
        'registration_plate': registration,
        'datetime_to_check': detection_time
    }
    res = requests.post("http://172.29.82.240:5050/car/check", json=payload)
    res = res.json()
    if('is_within' in res):
        if (res['is_within']):
            return True
    return False

def create_image(base64encoded):
    return base64.b64decode(base64encoded)

def create_image_name():
    file_uuid = uuid.uuid4()
    now = datetime.now()
    return f"{file_uuid}_{now.strftime('%Y5m%d_%H%M%S')}"

def save_image_to_local(image, file_name):
    with BytesIO(image) as f:
        save_image = Image.open(f)
        save_image.save(os.path.join(os.getcwd(), Config.UPLOAD_FOLDER, file_name + '.png',), format="PNG")