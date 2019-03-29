from app import db


class WishList(db.Model):
    __tablename__ = 'wishlist'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    item_id = db.Column(db.Integer)

    def __init__(self, item_id):
        self.item_id = item_id

