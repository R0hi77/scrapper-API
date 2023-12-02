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


#stores admin scrapes
class Job(db.Model):
    id = db.Column(db.Integer(),primary_key=True,autoincrement=True)
    role = db.Column(db.String(),nullable=False)
    description=db.Column(db.Text(),nullable=True)
    location =db.Column(db.Text(),nullable=True)
    company =db.Column(db.String(),nullable=True)
    requirements = db.Column(db.Text(),nullable=True)
    posted =db.Column(db.String(),nullable=True)


    def __repr__(self):
        return f"{self.id},{self.role},{self.description},{self.location},{self.company},{self.requirements},{self.posted}"

#stores user saved job
class Save(db.Model):
    id = db.Column(db.Integer(),primary_key=True,autoincrement=True)
    role = db.Column(db.String(),nullable=False)
    description=db.Column(db.Text(),nullable=True)
    location =db.Column(db.Text(),nullable=True)
    company =db.Column(db.String(),nullable=True)
    requirements = db.Column(db.Text(),nullable=True)
    posted =db.Column(db.String(),nullable=True)
    user_id = db.Column(db.String(),db.ForeignKey('user.id'),nullable=False)


    def __repr__(self):
        return str({
        'id': self.id,
        'role': self.role,
        'description': self.description,
        'location': self.location,
        'company': self.company,
        'requirements': self.requirements,
        'posted': self.posted
    })


class History(db.Model):
    id= db.Column(db.Integer(),primary_key=True,autoincrement=True)
    query_text=db.Column(db.String(),nullable=False)
    page=db.Column(db.Integer(),nullable=False)

    def __repr__(self):
        return f'{self.query},{self.page}'



class BlockedTokens(db.Model):
    id = db.Column(db.Integer(),primary_key=True,autoincrement=True)
    token=db.Column(db.String(),nullable=False)
    created =db.Column(db.DateTime(),default=datetime.utcnow())

    def __repr__(self):
          return f'{self.token}'

