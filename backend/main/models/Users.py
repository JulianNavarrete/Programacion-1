from .. import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    scores = db.relationship('Score', back_populates='user', cascade='all, delete-orphan')
    poems = db.relationship('Poem', back_populates='user', cascade='all, delete-orphan')

    @property
    def plain_password(self):
        raise AttributeError('Password is not a readable attribute')

    @plain_password.setter
    def plain_password(self, password):
        self.password = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        user_json = {
            'id': self.id,
            'name': self.name,
            'role': self.role,
            'email': self.email
        }
        return user_json

    def to_json(self):
        user_json = {
            'id': self.id,
            'name': self.name,
            'role': self.role,
            'email': self.email,
            'scores': [score.to_json() for score in self.scores],
            'poems': [poem.to_json() for poem in self.poems],
            'poem_amount': len(self.poems),
            'score_amount': len(self.scores)
        }
        return user_json

    def to_json_short(self):
        user_json = {
            'id': self.id,
            'name': self.name,
            'email': self.email,
        }
        return user_json

    @staticmethod
    def from_json(user_json):
        id = user_json.get('id')
        name = user_json.get('name')
        role = user_json.get('role')
        email = user_json.get('email')
        password = user_json.get('password')
        return User(id=id,
                    name=name,
                    role=role,
                    email=email,
                    plain_password=password
                    )

