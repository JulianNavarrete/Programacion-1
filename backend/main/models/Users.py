from .. import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(80), nullable=False)
    lastname = db.Column(db.String(80), nullable=False)
    role = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    scores = db.relationship('Score', back_populates='user', cascade='all, delete-orphan')
    poems = db.relationship('Poem', back_populates='user', cascade='all, delete-orphan')

    def __repr__(self):
        user_json = {
            'id': self.id,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'role': self.role,
            'email': self.email
        }
        return user_json

    def to_json(self):
        user_json = {
            'id': self.id,
            'firstname': self.firstname,
            'lastname': self.lastname,
            # 'role': self.role,
            'email': self.email,
            # 'password': self.password,
            'scores': [score.to_json() for score in self.scores],
            'poems': [poem.to_json() for poem in self.poems],
            'poem_amount': len(self.poems),
            'score_amount': len(self.scores)
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

