from flask_restful import Resource
from flask import request, jsonify
from datetime import datetime
from .. import db
from main.models import PoemModel


class Poem(Resource):

    def get(self, id):
        poem = db.session.query(PoemModel).get_or_404(id)
        return poem.to_json()

    def delete(self, id):
        poem = db.session.query(PoemModel).get_or_404(id)
        db.session.delete(poem)
        db.session.commit()
        return '', 204


class Poems(Resource):

    def get(self):
        page = 1
        per_page = 10
        poems = db.session.query(PoemModel)
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
                    poems = poems.filter(PoemModel.user.has(author).like('%' + value + '%'))

        poems = poems.paginate(page, per_page, True, 10)
        return jsonify({"poems": [poem.to_json_short() for poem in poems.items()],
                        "total": poems.total,
                        "pages": poems.pages,
                        "page": page})

    def post(self):
        poems = PoemModel.from_json(request.get_json())
        db.session.add(poems)
        db.session.commit()
        return poems.to_json(), 201

