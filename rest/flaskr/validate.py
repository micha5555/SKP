import re
def validateUsernameAndPassword(username: str,password: str):
    if not (re.match("^[A-Za-z0-9_.]+$",username)):
        return False
    if not (re.fullmatch(r'[A-Za-z0-9]{8,}',password)):
        return False
    sqlCommands = ["DROP","SELECT","UPDATE","DELETE","CREATE","INSERT","ALTER"]
    if any(command in username for command in sqlCommands):
        return False
    if any(command in password for command in sqlCommands):
        return False
    return True