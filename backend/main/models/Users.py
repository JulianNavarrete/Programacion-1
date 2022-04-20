from .. import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(80), nullable=False)
    lastname = db.Column(db.String(80), nullable=False)
    roll = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        user_json = {
            'id': self.id,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'roll': self.roll,
            'email': self.email
        }

    def to_json(self):
        user_json = {
            'id': self.id,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'roll': self.roll
        }
        return user_json

    @staticmethod
    def from_json(user_json):
        id = user_json.get('id')
        firstname = user_json.get('firstname')
        lastname = user_json.get('lastname')
        roll = user_json.get('roll')
        email = user_json.get('email')
        return User(id=id,
                    firstname=firstname,
                    lastname=lastname,
                    roll=roll,
                    email=email
                    )
