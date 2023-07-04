from flask_restful import Resource
from flask import request, jsonify
from datetime import datetime
from sqlalchemy import func
from .. import db
from main.models import PoemModel, UserModel, ScoreModel
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt


class Poem(Resource):

    @jwt_required()
    def get(self, id):
        poem = db.session.query(PoemModel).get_or_404(id)
        return poem.to_json()

    @jwt_required()
    def delete(self, id):
        claims = get_jwt()
        user_ident = get_jwt_identity()
        poem = db.session.query(PoemModel).get_or_404(id)
        if 'role' in claims:
            if claims['role'] == 'admin' or int(poem.userId) == user_ident:
                db.session.delete(poem)
                db.session.commit()
                return '', 204
            else:
                return 'You do not have permission to delete this poem'


class Poems(Resource):

    @jwt_required(optional=True)
    def get(self):
        page = 1
        per_page = 15
        poems = db.session.query(PoemModel)
        user_ident = get_jwt_identity()
        if user_ident:
            if request.get_json():
                filters = request.get_json().items()
                for key,value in filters:
                    if key == 'page':
                        page = int(value)
                    if key == 'per_page':
                        per_page = int(value)

            poems = db.session.query(PoemModel).filter(PoemModel.userId != user_ident)
            poems = poems.outerjoin(PoemModel.scores).group_by(PoemModel.id).order_by(func.count(PoemModel.scores))

        else:
            if request.get_json():
                filters = request.get_json().items()
                for key, value in filters:
                    if key == 'page':
                        page = int(value)
                    if key == 'per_page':
                        per_page = int(value)
                    if key == 'title':
                        poems = poems.filter(PoemModel.title.like('%' + value + '%'))
                    if key == 'userId':
                        poems = poems.filter(PoemModel.userId == value)
                    if key == 'date[gte]':
                        poems = poems.filter(PoemModel.date >= datetime.strptime(value, '%d-%m-%Y'))
                    if key == 'date[lte]':
                        poems = poems.filter(PoemModel.date <= datetime.strptime(value, '%d-%m-%Y'))
                    if key == 'author':
                        poems = poems.filter(PoemModel.user.has(UserModel.name.like('%' + value + '%')))

                    if key == 'sort_by':
                        if value == 'date':
                            poems = poems.order_by(PoemModel.date)
                        if value == 'date[desc]':
                            poems = poems.order_by(PoemModel.date.desc())
                        if value == 'score':
                            poems = poems.outerjoin(PoemModel.scores).group_by(PoemModel.id).order_by(func.avg(ScoreModel.score))
                        if value == 'score[desc]':
                            poems = poems.outerjoin(PoemModel.scores).group_by(PoemModel.id).order_by(func.avg(ScoreModel.score).desc())
                        if value == 'author':
                            poems = poems.outerjoin(PoemModel.user).group_by(PoemModel.id).order_by(UserModel.name)
                        if value == 'author[desc]':
                            poems = poems.outerjoin(PoemModel.user).group_by(PoemModel.id).order_by(UserModel.name.desc())

        poems = poems.paginate(page=page, per_page=per_page)
        return jsonify({"poems": [poem.to_json_short() for poem in poems.items],
                        "total": poems.total,
                        "pages": poems.pages,
                        "page": page})

    @jwt_required()
    def post(self):
        print("Llegué al post del back")
        user_ident = get_jwt_identity()
        poem = PoemModel.from_json(request.get_json())
        # user = db.session.query(UserModel).get_or_404(user_ident)
        # claims = get_jwt()
        print("user_ident:", user_ident)
        if user_ident:
            # if len(user.poems) >= 0:
            print("Entré al if")
            poem.userId = user_ident
            db.session.add(poem)
            print("Antes del commit")
            db.session.commit()
            return poem.to_json(), 201
            # else:
                # return 'There are not enough reviews from this user', 400
        else:
            return 'You are not a poet, only poets can create poems', 401

