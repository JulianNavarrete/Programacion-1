from .. import db


class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer, primary_Key=True)
    comment = db.Column(db.Integer, nullable=False)
    userId = db.Column(db.Integer)
    poemId = db.Column(db.Integer)

    def __repr__(self):
        score_json = {
            'userId': self.userId,
            'poemId': self.poemId,
            'comment': self.comment,
            'id': self.id,
            'score': self.score
        }
        return score_json

    def to_json(self):
        score_json = {
            'id': self.id,
            'score': self.score,
            'userId': self.userId
        }
        return score_json

    @staticmethod
    def from_json(score_json):
        id = score_json.get('id')
        score = score_json.get('score')
        comment = score_json.get('comment')
        userId = score_json.get('userId')
        poemId = score_json.get('poemId')
        return Score(id=id,
                     score=score,
                     comment=comment,
                     userId=userId,
                     poemId=poemId
                     )

