import re
from datetime import datetime


def validateLogin(login):
    if re.fullmatch(r'[A-Za-z0-9]{6,40}',login):
        return True
    return False

def validatePassword(password):
    passwdPattern= r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,40}$'
    if re.match(passwdPattern,password):
        return True
    return False

def validateName(name):
    if re.fullmatch(r'[A-Za-z]{1,40}',name):
        return True
    return False

def validateId(id):
    if isinstance(id, int):
        return True
    return False

def validateBoolean(param):
    if isinstance(param, bool):
        return True
    elif isinstance(param, str) and param.lower() in ['true', 'false']:
        return True
    else:
        return False

def validateDate(date):
    pattern = r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$'
    if re.match(pattern, date):
        return True
    return False

def validateLocalization(localization):
    pattern = "^[-]?\d{1,2}\.\d{6},[-]?\d{1,3}\.\d{6}$"
    if not re.match(pattern, location):
        return False
    
    lat, lon = location.split(",")
    lat_range = range(-90, 91)
    lon_range = range(-180, 181)
    if float(lat) not in lat_range or float(lon) not in lon_range:
        return False
    return True
    

def validateRegistration(register_plate):
    pattern = "^[A-Z]{1,3}[0-9A-Z]{2,9}$"
    if re.match(pattern, register_plate):
        return True
    return False

def validateProbability(probability):
    pattern = "^(100(\.00)?|[0-9]{1,2}(\.[0-9]{1,2})?)$"
    if re.match(pattern, str(probability)):
        return True
    return False
