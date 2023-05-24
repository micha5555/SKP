import jwt
from flask import session, request
from config import Config
from datetime import datetime, timedelta
from app.models.userModel import User
import functools

def tokenAdminRequire(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if not 'Access-token' in request.headers:
            return "Brak uprawnień", 403
        
        data = getDataFromToken(request.headers.get("Access-token"))
        if not data['is_admin']:
            return "Brak uprawnień", 403
        
        user = User.query.filter_by(id=data['id']).first()
        if user is None:
            return "Brak uprawnień", 403
        
        return view(data, **kwargs)
    return wrapped_view

def tokenUserRequire(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if not 'Access-token' in request.headers:
            return "Brak uprawnień", 403
        
        data = getDataFromToken(request.headers.get("Access-token"))
        if not data['is_controller'] and not data['is_admin']:
            return "Brak uprawnień", 403

        user = User.query.filter_by(id=data['id']).first()
        if user is None:
            return "Brak uprawnień", 403

        return view(data, **kwargs)
    return wrapped_view

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