# Auth example: https://github.com/miguelgrinberg/REST-auth/blob/master/api.py
from app import db
from flask import abort, request, jsonify, g, Blueprint
from flask_httpauth import HTTPBasicAuth
from sqlalchemy.exc import IntegrityError
from models.User import User

_user = Blueprint('_user', __name__)


auth = HTTPBasicAuth()


@_user.route('/api/users', methods=['POST'])
def new_user():
    email = request.args.get('email')
    password = request.args.get('password')
    name = request.args.get('name')
    if email is None or password is None or first_name is None:
        abort(400) # missing arguments
    user = User(email)
    user.hash_password(password)
    user.name = name

    db.session.add(user)
    try:
        db.session.commit()
    except IntegrityError:
        return jsonify(message="Email already signed up!"), 409
    return jsonify({'email': user.email, 'first_name': user.first_name, 'last_name': user.last_name}, 201)


@_user.route('/api/resource')
@auth.login_required
def get_resource():
    return jsonify({'data': 'Hello, %s!' % g.user.username})


@_user.route('/api/users/<int:id>')
def get_user(id):
    user = User.query.get(id)
    if not user:
        abort(400)
    return jsonify({'username': user.username})


@_user.route('/api/token', methods=['get'])
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token()
    return jsonify({ 'token': token.decode('ascii') })


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
