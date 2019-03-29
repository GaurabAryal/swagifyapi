import datetime
from app import db


class Item(db.Model):
    __tablename__ = 'item'

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(1000), unique=True)
    name = db.Column(db.String(500))
    price = db.Column(db.Float)
    website_name = db.Column(db.String(500))
    image = db.Column(db.String(1000))

    def __init__(self, url):
        self.url = url


