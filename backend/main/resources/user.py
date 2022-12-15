from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import UserModel
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from ..auth.decorators import admin_required, admin_or_poet_required


class User(Resource):

    @jwt_required()
    def get(self, id):
        user = db.session.query(UserModel).get_or_404(id)
        return user.to_json_short()

    @admin_or_poet_required
    def put(self, id):
        user = db.session.query(UserModel).get_or_404(id)
        data = request.get_json().items()
        for key, value in data:
            setattr(user, key, value)
        db.session.add(user)
        db.session.commit()
        return user.to_json_short(), 201

    @admin_or_poet_required
    def delete(self, id):
        user = db.session.query(UserModel).get_or_404(id)
        db.session.delete(user)
        db.session.commit()
        return '', 204


class Users(Resource):

    @admin_required
    def get(self):
        page = 1
        per_page = 15
        users = db.session.query(UserModel)
        if request.get_json():
            filters = request.get_json().items()
            for key, value in filters:
                if key == 'page':
                    page = int(value)
                if key == 'per_page':
                    per_page = int(value)
                if key == 'name':
                    users = users.filter(UserModel.name.like('%' + value + '%'))

                if key == 'sort_by':
                    if value == 'name':
                        users = users.order_by(UserModel.name)
                    if value == 'name[desc]':
                        users = users.order_by(UserModel.name.desc())

            users = users.paginate(page, per_page, True, 10)
            return jsonify({'users': [user.to_json_short() for user in users.items],
                            'total': users.total,
                            'pages': users.pages,
                            'page': page})


'''
    def post(self):
        users = UserModel.from_json(request.get_json())
        db.session.add(users)
        db.session.commit()
        return users.to_json(), 201
'''
