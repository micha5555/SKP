import os
import jwt
import uuid
import base64
import datetime
import requests
import random
from flask import g, session, make_response
from datetime import datetime, timezone, timedelta
from PIL import Image
from io import BytesIO
from werkzeug.security import check_password_hash
from config import Config

def makeResponse(response_data, code):
    response = make_response(response_data)
    response.headers['Content-Type'] = 'application/json'
    return response, code

def getRequestData(request):
    if (Config.REQUEST_METHOD_TYPE == "form"):
        return request.form
    else:
        return request.get_json()

def checkPassword(password,pwhash):
    return check_password_hash(pwhash,password)

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
    return all(element in elements for element in lst)

def checkIfPaid(registration, detection_time):
    # here will be created element which will check if element was paid or not 
    r = random.random()
    #print(r)
    if r > 0.5:
        return False
    return True
    # payload = {
        # 'registration_plate': registration,
        # 'datetime_to_check': detection_time
    # }
    # res = requests.post("http://localhost:5050/car/check", json=payload)
    # res = res.json()
    # if('is_within' in res):
        # if (res['is_within']):
            # return True
    # return False

def create_image(base64encoded):
    return base64.b64decode(base64encoded)

def getUuid():
    return str(uuid.uuid4())[:6]

def create_image_name():
    file_uuid = getUuid()
    now = datetime.now()
    return f"{file_uuid}_{now.strftime('%Y%m%d_%H%M%S')}"

def save_image_to_local(file, file_name):
    if Config.REQUEST_METHOD_TYPE == "form":
        file.save(os.path.join(
            os.getcwd(), 
            Config.UPLOAD_FOLDER, 
            file_name + '.png',
        ))
    else:
        # nie testowałem jeszcze 
        with BytesIO(create_image(file)) as f:
            save_image = Image.open(f)
            save_image.save(os.path.join(os.getcwd(), Config.UPLOAD_FOLDER, file_name + '.png',), format="PNG")