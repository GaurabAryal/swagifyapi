# Auth example: https://github.com/miguelgrinberg/REST-auth/blob/master/api.py
from app import db
from flask import abort, request, jsonify, g, Blueprint
from sqlalchemy.exc import IntegrityError
from sqlalchemy.exc import SQLAlchemyError
from models.Item import Item
from models.Wishlist import WishList
from models.User import User
from resources.security import auth

item = Blueprint('item', __name__)


@item.route('/api/item', methods=['POST'])
@auth.login_required
def add_item():
    url = request.args.get('url')
    name = request.args.get('name')
    price = float(request.args.get('price'))
    website_name = request.args.get('website_name')
    image = request.args.get('image_url')
    if url is None or name is None or price is None or website_name is None:
        abort(400) # missing arguments
    _item = Item(url)
    _item.name = name
    _item.price = price
    _item.website_name = website_name
    _item.image = image

    db.session.add(_item)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        existing_item = _item.query.filter_by(url=url).first()
        return jsonify({'data': 'Failed to add Item!', 'item_id': existing_item.id, 'price': existing_item.price}), 409
    return jsonify({'data': 'Successfully added Item!'}), 201


@item.route('/api/item/', methods=['GET'])
def search_item():
    name = request.args.get('name')
    query = db.session.query(Item).\
        filter(Item.name.ilike('%' + name + '%')).\
        all()
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


@item.route('/api/item/<int:item_id>', methods=['PUT'])
def updates_item(item_id):
    _item = Item.query.filter_by(id=item_id).first()
    _item.price = float(request.args.get('price'))

    try:
        db.session.commit()
    except SQLAlchemyError as e:
        return jsonify(message="Error saving to database."), 500

    query = db.session.query(User).\
        join(WishList, WishList.user_id == User.id).\
        filter(WishList.item_id == item_id)

    email_array = []
    for row in query:
        email_array.append(row.email)

    return jsonify({'data': 'Successfully updated item!', 'emails': email_array}), 201


@item.route('/api/item/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    Item.query.filter_by(id=item_id).delete()
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        return jsonify(message="Error saving to database."), 500

    return jsonify({'data': 'Successfully deleted item!'}), 201
