from flask_restful import Resource, reqparse
from thflask.models.user import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("username", required=True, type=str, help="Please give a username")
    parser.add_argument("password", required=True, type=str, help="Please give a password")

    def post(self):
        data = UserRegister.parser.parse_args()
        if UserModel.find_by_username(data["username"]):
            return f"User {data['username']} already exists", 400

        user = UserModel(**data)
        user.store_user()

        return f"User {data['username']} created succesfully", 201
