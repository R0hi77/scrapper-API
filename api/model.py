from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer(),primary_key=True,autoincrement=True)
    username = db.Column(db.String(),nullable=False)
    email = db.Column(db.String(),nullable=False, unique=True)
    password=db.Column(db.String(),nullable=False)
    created = db.Column(db.DateTime(),default=datetime.utcnow())

    def __repr__(self):
        return f"{self.id},{self.username},{self.email},{self.created},{self.id}"



class Job(db.Model):
    id = db.Column(db.Integer(),primary_key=True,autoincrement=True)
    role = db.Column(db.String(),nullable=False)
    description=db.Column(db.String(),nullable=True)
    location =db.Column(db.String(),nullable=True)
    company =db.Column(db.String(),nullable=True)
    requirements = db.Column(db.String(),nullable=True)
    posted =db.Column(db.String(),nullable=True)
    user_id = db.Column(db.Integer(),db.ForeignKey('user.id'),nullable=False)


    def __repr__(self):
        return f"{self.id},{self.role},{self.description},{self.location},{self.company},{self.requirements},{self.posted}"



class BlockedTokens(db.Model):
    id = db.Column(db.Integer(),primary_key=True,autoincrement=True)
    token=db.Column(db.String(),nullable=False)
    created =db.Column(db.DateTime(),default=datetime.utcnow())

    def __repr__(self):
          return f'{self.token}'

