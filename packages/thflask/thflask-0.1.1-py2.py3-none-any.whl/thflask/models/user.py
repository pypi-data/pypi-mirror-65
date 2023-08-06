from uuid import uuid4
from thflask.db import db


class UserModel(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Text, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __init__(self, username, password, _id=None):
        self.username = username
        self.password = password
        if not _id:
            _id = str(uuid4())
        self.id = _id

    @classmethod
    def find_by_username(cls, username):
        """
        Class function that is called by a process and is looking for the user in the
        database based on the username, and if it finds it, it creates an object of this
        user and returns it
        """
        user = cls.query.filter_by(username=username).first()
        return user

    @classmethod
    def find_by_id(cls, _id):
        """
        Class function that is called by a process and is looking for the user in the
        database based on the id, and if it finds it, it creates an object of this
        user and returns it
        """
        user = cls.query.filter_by(id=_id).first()
        return user

    def store_user(self):
        db.session.add(self)
        db.session.commit()
