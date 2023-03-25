import re
from datetime import datetime
def validateLogin(login):
    if(re.fullmatch(r'[A-Za-z0-9]{6,40}',login)):
        return True
    return False

def validatePassword(password):
    passwdPattern= r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,40}$'
    if (re.match(passwdPattern,password)):
        return True
    return False

def validateName(name):
    if(re.fullmatch(r'[A-Za-z]{1,40}',name)):
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
    pass

def validateLocalization(localization):
    pass
    