import re
def validateLogin(login):
    if(re.fullmatch(r'[A-Za-z0-9]{1,}',login)):
        return True
    return False

def validatePassword(password):
    passwdPattern="^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9]).{8,20}$"
    if (re.match(passwdPattern,password)):
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
    