from flask_restful import Resource
from flask import request

# Test dictionary
POEMS = {
    1: {'Title': 'Elegía', 'Author': 'Miguel'},
    2: {'Title': 'Tú me quieres blanca', 'Author': 'Alfonsina'},
    3: {'Title': 'Gacela de la terrible presencia', 'Author': 'Federico'},
    4: {'Title': 'Me gusta cuando callas', 'Author': 'Pablo'},
    5: {'Title': 'Amor constante más allá de la muerte', 'Author': 'Francisco'}
}


class Poem(Resource):
    def get(self, id):
        if int(id) in POEMS:
            return POEMS[int(id)]
        return '', 404

    def delete(self, id):
        if int(id) in POEMS:
            del POEMS[int(id)]
            return '', 204
        return '', 404


class Poems(Resource):
    def get(self):
        return POEMS

    def post(self):
        poem = request.get_json()
        id = int(max(POEMS)) + 1
        POEMS[id] = poem
        return POEMS[id], 201

