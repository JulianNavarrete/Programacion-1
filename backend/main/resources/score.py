from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import ScoreModel


class Score(Resource):

    def get(self, id):
        score = db.session.query(ScoreModel).get_or_404(id)
        return score.to_json()

    def delete(self, id):
        score = db.session.query(ScoreModel).get_or_404(id)
        db.session.delete(score)
        db.session.commit()
        return '', 204


class Scores(Resource):

    def get(self):
        page = 1
        per_page = 10
        scores = db.session.query(ScoreModel)
        if request.get_json():
            filters = request.get_json().items()
            for key, value in filters:
                if key == 'page':
                    page = int(value)
                if key == 'per_page':
                    per_page = value
        return jsonify([score.to_json_short() for score in scores])

    def post(self):
        score = ScoreModel.from_json(request.get_json())
        db.session.add(score)
        db.session.commit()
        return score.to_json(), 201

