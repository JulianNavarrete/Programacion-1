from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import ScoreModel
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from ..auth.decorators import poet_required


class Score(Resource):

    @jwt_required()
    def get(self, id):
        score = db.session.query(ScoreModel).get_or_404(id)
        return score.to_json()

    @jwt_required()
    def delete(self, id):
        claims = get_jwt()
        user_ident = get_jwt_identity()
        score = db.session.query(ScoreModel).get_or_404(id)
        if 'role' in claims:
            if claims['role'] == 'admin' or int(score.userId) == user_ident:
                db.session.delete(score)
                db.session.commit()
                return '', 204
            else:
                return 'Only admins and the score owner can delete scores', 403

    @jwt_required()
    def put(self, id):
        user_ident = get_jwt_identity()
        score = db.session.query(ScoreModel).get_or_404(id)
        if user_ident == score.user_id:
            data = request.get_json().items()
            for key, value in data:
                if key == 'score':
                    setattr(score, key, value)
                db.session.add(score)
                db.session.commit()
                return score.to_json(), 201
        else:
            return 'Only the score owner can update scores', 403


class Scores(Resource):

    @jwt_required()
    def get(self):
        scores = db.session.query(ScoreModel).all()
        return jsonify([score.to_json_short() for score in scores])

    @poet_required
    def post(self):
        user_ident = get_jwt_identity()
        score = ScoreModel.from_json(request.get_json())
        score.userId = user_ident
        db.session.add(score)
        db.session.commit()
        return score.to_json(), 201

