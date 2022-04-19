from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import ScoreModel


class Score(Resource):
    def get(self, id):
        pass

    def delete(self, id):
        pass


class Scores(Resource):
    def get(self):
        pass

    def post(self):
        pass

