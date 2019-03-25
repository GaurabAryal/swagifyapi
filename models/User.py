import datetime
from app import db, application
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)


# User Model example: https://github.com/miguelgrinberg/REST-auth/blob/master/api.py

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    username = db.Column(db.String(255), unique=True)
    name = db.Column(db.String(100))
    password_hash = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    active = db.Column(db.Boolean)

    def __init__(self, email):
        self.email = email
        self.username = email
        self.active = True

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration=7200):
        s = Serializer(application.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(application.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None    # valid token, but expired
        except BadSignature:
            return None    # invalid token
        user = User.query.get(data['id'])

        return user
