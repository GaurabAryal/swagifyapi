
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import os


application = Flask(__name__)
application.config['SECRET_KEY'] = os.environ['SECRET_KEY']
application.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']

db = SQLAlchemy(application)



if __name__ == "__main__":
    application.run(host='0.0.0.0')
