from flask_restful import Resource
from flask import request

# Test dictionary
USERS = {
    1: {'firstname': 'Sacha', 'lastname': 'Fenske'},
    2: {'firstname': 'Santiago', 'lastname': 'Moyano'},
    3: {'firstname': 'Lucas', 'lastname': 'Galdame'},
    4: {'firstname': 'Bruno', 'lastname': 'Romero'},
    5: {'firstname': 'Douglas', 'lastname': 'Arenas'}
}


class User(Resource):
    def get(self, id):
        if int(id) in USERS:
            return USERS[int(id)]
        return '', 404

    def delete(self, id):
        if int(id) in USERS:
            del USERS[int(id)]
            return '', 204
        return '', 404


class Users(Resource):
    def get(self):
        return USERS

    def post(self):
        user = request.get_json()
        id = int(max(USERS)) + 1
        USERS[id] = user
        return USERS[id], 201

