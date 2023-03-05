import functools
from flask import g,session, redirect, url_for
import jwt
from datetime import datetime, timedelta
from __init__ import app


def generate_jwt(payload, lifetime=None):
    if lifetime:
        payload['exp'] = datetime.now() + timedelta(minutes=lifetime)
    jwt_token= jwt.encode(payload, app.config['SECRET_KEY'], algorithm="HS256")
    refresh_payload={'session_id':session.get("session_id"),
                     'exp':datetime.now() + timedelta(days=1)
                     }
    refresh_token= jwt.encode(refresh_payload, app.config['SECRET_KEY'], algorithm="HS256")
    return{jwt_token,refresh_token}

def decode_jwt(token):
    return jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])

def refresh_jwt(jwt_token,refresh_token, lifetime=None):
    token=decode_jwt(refresh_jwt)
    if(token['session_id']==session.get("session_id")):
        jwt=decode_jwt(jwt_token)
        jwt['exp']= datetime.now() + timedelta(minutes=lifetime)
        jwt_token_new= jwt.encode(jwt, app.config['SECRET_KEY'], algorithm="HS256")
        return{jwt_token_new,refresh_token}

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('user.login'))
        return view(**kwargs)
    return wrapped_view