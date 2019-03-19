# Auth example: https://github.com/miguelgrinberg/REST-auth/blob/master/api.py

from flask import Flask, abort, request, jsonify, g, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth

import json
import os


application = Flask(__name__)
application.config['SECRET_KEY'] = os.environ['SECRET_KEY']
application.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']

db = SQLAlchemy(application)

from models import User
auth = HTTPBasicAuth()


@application.route("/")
def hello():
    return "<h1 style='color:blue'>Hello There!</h1>"


@application.route("/login")
def login():
        return json.dumps({ "data": "logged in successfully" }), 200


@application.route("/signup", methods=['POST'])
def signup():
        return json.dumps({ "data": "cant sign up!" }), 400


@application.route('/api/users', methods = ['POST'])
def new_user():
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        abort(400) # missing arguments
    if User.query.filter_by(username = username).first() is not None:
        abort(400) # existing user
    user = User(username = username)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({ 'username': user.username }), 201, {'Location': url_for('get_user', id = user.id, _external = True)}


@application.route('/api/resource')
@auth.login_required
def get_resource():
    return jsonify({'data': 'Hello, %s!' % g.user.username})


@application.route('/api/users/<int:id>')
def get_user(id):
    user = User.query.get(id)
    if not user:
        abort(400)
    return jsonify({'username': user.username})

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

if __name__ == "__main__":
    application.run(host='0.0.0.0')
