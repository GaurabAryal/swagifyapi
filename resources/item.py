# Auth example: https://github.com/miguelgrinberg/REST-auth/blob/master/api.py
from app import db
from flask import abort, request, jsonify, g, Blueprint
from sqlalchemy.exc import IntegrityError
from models.Item import Item
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
        return jsonify(message="Item with this URL already exists!"), 409
    return jsonify({'data': 'Successfully added Item!'}), 201

