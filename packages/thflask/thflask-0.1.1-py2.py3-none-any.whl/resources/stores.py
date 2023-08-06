from flask_restful import Resource, reqparse
from models.stores import StoreModel, StoreListModel


class Store(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("name", required=True, type=str, help="Name is required")

    def get(self, name):
        store = StoreModel.retrieve_store(name)
        return (store.json(), 200) if store else ("Store not found", 404)

    def post(self, name):
        if StoreModel.retrieve_store(name):
            return f"Store {name} already exists", 400

        data = self.parser.parse_args()
        store = StoreModel(**data)
        store.store_store()
        return store.json(), 201

    def delete(self, name):
        store = StoreModel.retrieve_store(name)
        if not store:
            return f"Store {name} not found", 404

        store.remove_store()
        return "Deleted", 200


class StoreList(Resource):
    def get(self):
        return (StoreListModel.get_list(), 200) or ([], 200)
