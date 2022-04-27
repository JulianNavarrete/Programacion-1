from .. import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(80), nullable=False)
    lastname = db.Column(db.String(80), nullable=False)
    role = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    score = db.relationship('Score', backpopulate='user', cascade='all, delete-orphan')
    poem = db.relationship('Poem', backpopulate='user', cascade='all, delete-orphan')

    def __repr__(self):
        user_json = {
            'id': self.id,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'role': self.role,
            'email': self.email
        }

    def to_json(self):
        user_json = {
            'id': self.id,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'role': self.role,
            'email': self.email,
            'password': self.password,
            'score': [score.to_json() for score in self.score],
            'poem': [poem.to_json() for poem in self.poem]
        }
        return user_json

    def to_json_short(self):
        user_json = {
            'id': self.id,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'role': self.role,
            'email': self.email,
            'password': self.password
        }
        return user_json

    @staticmethod
    def from_json(user_json):
        id = user_json.get('id')
        firstname = user_json.get('firstname')
        lastname = user_json.get('lastname')
        role = user_json.get('role')
        email = user_json.get('email')
        password = user_json.get('password')
        return User(id=id,
                    firstname=firstname,
                    lastname=lastname,
                    role=role,
                    email=email,
                    password=password
                    )

