import re
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

def validateFileName(filename):
    pass

def validateId(id):
    pass

def validateBoolean(param):
    pass

def validateDate(date):
    pass

def validateLocalization(localization):
    pass
    