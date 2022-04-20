from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import UserModel


class User(Resource):
    def get(self, id):
        user = db.session.query(UserModel).get_or_404(id)
        return user.to_json()

    def delete(self, id):
        user = db.session.query(UserModel).get_or_404(id)
        db.session.delete(user)
        db.session.commit()
        return '', 204


class Users(Resource):
    def get(self):
        users = db.session.query(UserModel).all()
        return jsonify([user.to_json_short() for user in users])

    def post(self):
        users = UserModel.from_json(request.get_json())
        db.session.add(users)
        db.session.commit()
        return users.to_json(), 201

