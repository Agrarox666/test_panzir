import sqlalchemy as db
from flask_jwt_extended import create_access_token
from datetime import timedelta
from passlib.hash import bcrypt


class Task:
    def __init__(self, id, title, description, done):
        self.id = id
        self.title = title
        self.description = description
        self.done = done


from app.routes import Base


class User(Base):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), nullable=False)
    password = db.Column(db.String(250), nullable=False)

    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.email = kwargs.get('email')
        self.password = bcrypt.hash(kwargs.get('password'))

    def get_token(self, expire_time=24):
        token = create_access_token(
            identity=self.id, expires_delta=timedelta(expire_time))
        return token

    @classmethod
    def authenticate(cls, email, password):
        user = cls.query.filter(cls.email == email)
        if not bcrypt.verify(password, user.password):
            raise Exception('Incorrect password!')
        return user
