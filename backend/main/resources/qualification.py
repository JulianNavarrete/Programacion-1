from flask_restful import Resource
from flask import request

# Test dictionary
QUALIFICATIONS = {
    1: {'qualification': 3},
    2: {'qualification': 4},
    3: {'qualification': 5}
}


class Qualification(Resource):
    def get(self, id):
        if int(id) in QUALIFICATIONS:
            return QUALIFICATIONS[int(id)]
        return '', 404

    def delete(self, id):
        if int(id) in QUALIFICATIONS:
            del QUALIFICATIONS[int(id)]
            return '', 204
        return '', 404


class Qualifications(Resource):
    def get(self):
        return QUALIFICATIONS

    def post(self):
        qualification = request.get_json()
        id = int(max(QUALIFICATIONS)) + 1
        QUALIFICATIONS[id] = qualification
        return QUALIFICATIONS[id], 201

