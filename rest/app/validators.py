import re
from datetime import datetime
polish_chars = 'AaĄąBbCcĆćDdEeĘęFfGgHhIiJjKkLlŁłMmNnŃńOoÓóPpRrSsŚśTtUuWwYyZzŹźŻż'

def validateLogin(login):
    if re.fullmatch(r'[A-Za-z0-9]{4,40}', login):
        return True
    return False

def validatePassword(password):
    passwdPattern= r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,40}$'
    if re.match(passwdPattern,password):
        return True
    return False

def validateName(name):
    if re.fullmatch(r'[A-Za-zAaĄąBbCcĆćDdEeĘęFfGgHhIiJjKkLlŁłMmNnŃńOoÓóPpRrSsŚśTtUuWwYyZzŹźŻż]{1,40}', name):
        return True
    return False

def validateId(id):
    if re.match(r'\d+', id):
        return True
    return False

def validateBoolean(param):
    if isinstance(param, bool) or param in [0, 1]:
        return True
    elif isinstance(param, str) and param.lower() in ['true', 'false','0','1']:
        return True
    return False

def validateDate(date):
    pattern = r'^\d{4}-\d{2}-\d{2}'
    if re.match(pattern, date):
        return True
    return False

def validateLocalization(localization):
    pattern = r'^[-]?\d{1,2}\.\d{6},[-]?\d{1,3}\.\d{6}$'
    if not re.match(pattern, localization):
        return False
    
    lat, lon = localization.split(",")
    lat = float(lat)
    lon = float(lon)
    if lat < 91 and lat > -90 and -180 < lon and lon < 181:
        return True
    return False

def validateRegistration(register_plate):
    pattern = "^[A-Z]{1,3}[0-9A-Z]{2,9}$"
    if re.match(pattern, register_plate):
        return True
    return False

def validateProbability(probability):
    pattern = "^(100(\.00)?|[0-9]{1,3}(\.[0-9]{1,2})?)$"
    if re.match(pattern, str(probability)):
        return True
    return False
