from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel, ItemListModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "price", required=True, type=float, help="Please give a price for this item"
    )
    parser.add_argument(
        "store_id", required=True, type=str, help="Please insert the store for this item"
    )

    def get(self, name):
        item = ItemModel.retrieve_item(name)
        return (item.json(), 200) if item else ("Not found", 404)

    @jwt_required()
    def post(self, name):
        if ItemModel.retrieve_item(name):
            return f"Item with name {name} already exists", 400

        data = Item.parser.parse_args()
        data["name"] = name
        if not data:
            return "Incorrect data", 400
        item = ItemModel(**data)
        item.store_item()
        return item.json(), 201

    @jwt_required()
    def delete(self, name):
        item = ItemModel.retrieve_item(name)
        if not item:
            return "Item not found", 404
        item.remove_item()
        return f"Removed item {name}", 200

    @jwt_required()
    def put(self, name):
        data = Item.parser.parse_args()
        data["name"] = name
        if not data:
            return "Incorrect data", 400
        item = ItemModel.retrieve_item(name)
        if not item:
            new_item = ItemModel(**data)
            new_item.store_item()
            return (f"Created item {name}", 201)
        else:
            item.update_item(**data)
            return f"Updated item {name}", 200


class ItemList(Resource):
    def get(self):
        item_list = ItemListModel.retrieve_item_list() or []
        return item_list, 200
