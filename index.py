
from flask import jsonify
from app import db, application

import json


@application.route('/')
def ind():
    return jsonify({'data': 'Welcome to Swagify API!'})

