from uuid import uuid1
from db import db


class ItemModel(db.Model):
    __tablename__ = "items"
    id = db.Column(db.Text, primary_key=True)
    name = db.Column(db.String(20))
    price = db.Column(db.Float(precision=2))

    store_id = db.Column(db.Text, db.ForeignKey("stores.id"))
    store = db.relationship("StoreModel")

    def __init__(self, name, price, store_id, _id=None):
        self.name = name
        self.price = price
        self.store_id = store_id
        if not _id:
            self.id = str(uuid1())

    @classmethod
    def retrieve_item(cls, name):
        # Get the Item from the database
        item = cls.query.filter_by(name=name).first()
        return item

    def store_item(self):
        db.session.add(self)
        db.session.commit()

    def remove_item(self):
        db.session.delete(self)
        db.session.commit()

    def update_item(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id
        self.store_item()

    def json(self):
        return {"name": self.name, "price": self.price, "store": self.store_id}


class ItemListModel():
    @classmethod
    def retrieve_item_list(cls):
        item_list = ItemModel.query.all()
        return [item.json() for item in item_list]
