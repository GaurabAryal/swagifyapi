# Auth example: https://github.com/miguelgrinberg/REST-auth/blob/master/api.py
from app import db
from flask import abort, request, jsonify, g, Blueprint
from sqlalchemy.exc import SQLAlchemyError
from models.Wishlist import WishList
from models.Item import Item
from resources.security import auth

wishlist = Blueprint('wishlist', __name__)


@wishlist.route('/api/wishlist/<int:item_id>', methods=['POST'])
@auth.login_required
def add_item(item_id):
    _wishlist = WishList(item_id)
    _wishlist.item_id = item_id
    _wishlist.user_id = g.user.id
    record_exists = db.session.query(WishList).filter_by(user_id=g.user.id, item_id=item_id).scalar() is not None
    if record_exists:
        return jsonify(message="The item was already in the database"), 409

    db.session.add(_wishlist)
    try:
        db.session.commit()
    except SQLAlchemyError:
        return jsonify(message="Error saving to database."), 500
    return jsonify({'data': 'Successfully added item to wishlist!'}), 201


@wishlist.route('/api/wishlist', methods=['GET'])
@auth.login_required
def get_items():
    query = db.session.query(Item).\
        join(WishList, WishList.item_id == Item.id).\
        filter(WishList.user_id == g.user.id)
    res = []
    # query = query.order_by(Item.name).all()
    for ind, row in enumerate(query):
        _item = {}
        _item['id'] = row.id
        _item['name'] = row.name
        _item['checkoutUrl'] = row.url
        _item['brand'] = row.website_name
        _item['price'] = row.price
        _item['imageUrl'] = row.image
        res.append(_item)
    return jsonify({'data': res}), 200


@wishlist.route('/api/wishlist/<int:_item_id>', methods=['DELETE'])
@auth.login_required
def delete_item(_item_id):
    WishList.query.filter_by(item_id=_item_id, user_id=g.user.id).delete()
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print(error)
        return jsonify(message="Error saving to database."), 500

    return jsonify({'data': 'Successfully deleted item from wishlist!'}), 201

