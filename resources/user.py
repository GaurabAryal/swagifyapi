# Auth example: https://github.com/miguelgrinberg/REST-auth/blob/master/api.py
from app import db
from flask import abort, request, jsonify, g, Blueprint
from sqlalchemy.exc import IntegrityError
from models.User import User
from resources.security import auth

_user = Blueprint('_user', __name__)


@_user.route('/api/users', methods=['POST'])
def new_user():
    email = request.args.get('email')
    password = request.args.get('password')
    name = request.args.get('name')
    if email is None or password is None or name is None:
        abort(400) # missing arguments
    user = User(email)
    user.hash_password(password)
    user.name = name

    db.session.add(user)
    try:
        db.session.commit()
    except IntegrityError:
        return jsonify(message="Email already signed up!"), 409
    return jsonify({'data': 'Successfully registered!'}), 201


@_user.route('/api/resource')
@auth.login_required
def get_resource():
    return jsonify({'data': 'Hello, %s!' % g.user.username})


@_user.route('/api/token', methods=['get'])
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token()
    return jsonify({'token': token.decode('ascii'), 'name': g.user.name}), 200


