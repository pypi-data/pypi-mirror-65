from uuid import uuid4
from db import db


class StoreModel(db.Model):
    __tablename__ = "stores"
    id = db.Column(db.Text, primary_key=True)
    name = db.Column(db.String(20))

    items = db.relationship("ItemModel", lazy="dynamic")

    def __init__(self, name, _id=None):
        self.name = name
        if not _id:
            self.id = str(uuid4())

    @classmethod
    def retrieve_store(cls, name):
        store = cls.query.filter_by(name=name).first()
        return store

    def store_store(self):
        db.session.add(self)
        db.session.commit()

    def remove_store(self):
        db.session.delete(self)
        db.session.commit()

    def json(self):
        return {
            "store_id": self.id,
            "name": self.name,
            "items": [item.json() for item in self.items.all()],
        }


class StoreListModel:
    @classmethod
    def get_list(cls):
        store_list = StoreModel.query.all()
        return [x.json() for x in store_list]
