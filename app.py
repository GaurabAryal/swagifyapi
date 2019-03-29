
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import os


application = Flask(__name__)
application.config['SECRET_KEY'] = os.environ['SECRET_KEY']
application.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']

db = SQLAlchemy(application)

# Import exception to remove circular dependency
from resources.user import _user
from resources.item import item
from resources.wishlist import wishlist

application.register_blueprint(_user)
application.register_blueprint(item)
application.register_blueprint(wishlist)


if __name__ == "__main__":
    application.run(host='0.0.0.0')
