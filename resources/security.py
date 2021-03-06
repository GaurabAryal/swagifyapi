# Auth example: https://github.com/miguelgrinberg/REST-auth/blob/master/api.py
from app import db

from flask_httpauth import HTTPBasicAuth
from flask import g
from models.User import User
auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    user = User.verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = User.query.filter_by(username=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True
