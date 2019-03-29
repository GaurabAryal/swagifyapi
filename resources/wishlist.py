# Auth example: https://github.com/miguelgrinberg/REST-auth/blob/master/api.py
from app import db
from flask import abort, request, jsonify, g, Blueprint
from sqlalchemy.exc import SQLAlchemyError
from models.Wishlist import WishList
from models.User import User
from models.Item import Item
from resources.security import auth

wishlist = Blueprint('wishlist', __name__)


@wishlist.route('/api/wishlist/<int:item_id>', methods=['POST'])
@auth.login_required
def add_item(item_id):
    _wishlist = WishList(item_id)
    _wishlist.item_id = item_id
    _wishlist.user_id = g.user.id
    record_exists = db.session.query(User.id).filter_by(user_id=g.user.id, item_id=item_id).scalar() is not None
    if record_exists:
        return jsonify(message="The item was already in the database"), 409

    db.session.add(_wishlist)
    try:
        db.session.commit()
    except SQLAlchemyError:
        return jsonify(message="Error saving to database."), 500
    return jsonify({'data': 'Successfully added item to wish list!'}), 201


@wishlist.route('/api/wishlist', methods=['GET'])
@auth.login_required
def get_items():
    query = db.session.query(Item).\
        join(WishList, WishList.item_id == Item.id).\
        filter(WishList.user_id == g.user.id)
    for row in query:
        print(row.name)
