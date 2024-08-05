from . import db

class Influencers(db.Model):
    __tablename__ = 'influencers'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    account = db.Column(db.String(100), nullable=False)
    
class Sponsors(db.Model):
    __tablename__ = 'sponsors'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    website = db.Column(db.String(100), nullable=False)
