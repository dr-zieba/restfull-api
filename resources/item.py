from flask_restful import reqparse, Resource
from flask_jwt import jwt_required
from models.item import ItemModel
from db import db

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="Price filed can not be empty!"
    )
    parser.add_argument('store_id',
        type=int,
        required=True,
        help="Store filed can not be empty!"
    )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': 'Item already exists'}

        data = Item.parser.parse_args()
        item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except:
            return {'message': 'An error occured'}, 500

        return {'message':'Item created'}, 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message': 'Item {} removed'.format(name)}, 200

    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']

        item.save_to_db()

        return item.json()


class Items(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}
