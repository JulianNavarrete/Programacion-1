import statistics
from .. import db
import datetime as dt


class Poem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    body = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, default=dt.datetime.now(), nullable=False)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', back_populates='poems', uselist=False, single_parent=True)
    scores = db.relationship('Score', back_populates='poem', cascade='all, delete-orphan')

    def __repr__(self):
        poem_json = {
            'id': self.id,
            'title': self.title,
            'body': self.body,
            'date': self.date,
            'userId': self.userId,
        }
        return poem_json

    def get_average_score(self):
        if len(self.scores) == 0:
            return 0
        else:
            scores_list = []
            for score in self.scores:
                scores_list.append(score.score)
            return statistics.mean(scores_list)

    def get_amount_score(self):
        return int(len(self.scores))

    def to_json(self):
        poem_json = {
            'id': self.id,
            'title': self.title,
            'body': self.body,
            'date': str(self.date.strftime('%Y-%m-%d %H:%M:%S')),
            'user': self.user.to_json_short(),
            'scores': [score.to_json_short() for score in self.scores],
            'amt_scores': self.get_amount_score(),
            'avg_score': self.get_average_score(),
        }
        return poem_json

    def to_json_short(self):
        poem_json = {
            'id': self.id,
            'title': self.title,
            'body': self.body,
            'user': self.user.to_json_short(),
            'date': str(self.date.strftime('%Y-%m-%d %H:%M:%S')),
            'avg_score': self.get_average_score(),
        }
        return poem_json

    @staticmethod
    def from_json(poem_json):
        id = poem_json.get('id')
        title = poem_json.get('title')
        body = poem_json.get('body')
        userId = poem_json.get('userId')
        return Poem(id=id,
                    title=title,
                    body=body,
                    userId=userId
                    )

