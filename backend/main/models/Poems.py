import statistics
from .. import db


class Poem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    body = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backpopulate='poem', uselist=False, single_parent=True)
    score = db.relationship('Score', backpopulate='poem', cascade='all, delete-orphan')

    def __repr__(self):
        poem_json = {
            'id': self.id,
            'title': self.title,
            'body': self.body,
            'date': self.date,
            'userId': self.userId,
        }
        return poem_json

    def to_json(self):

        scores_list = []
        for score in self.scores:
            scores_list.append(score.score)
        avg_score = statistics.mean(scores_list)

        poem_json = {
            'id': self.id,
            'title': self.title,
            'body': self.body,
            'date': str(self.date.strftime('%Y-%m-%d %H:%M:%S')),
            'user': self.user.to_json_short(),
            'score': avg_score
        }
        return poem_json

    def to_json_short(self):
        poem_json = {
            'title': self.title,
            'body': self.body,
            'date': str(self.date.strftime('%Y-%m-%d %H:%M:%S')),
        }
        return poem_json

    @staticmethod
    def from_json(poem_json):
        id = poem_json.get('id')
        title = poem_json.get('title')
        body = poem_json.get('body')
        date = poem_json.get('date')
        userId = poem_json.get('userId')
        return Poem(id=id,
                    title=title,
                    body=body,
                    date=date,
                    userId=userId
                    )

