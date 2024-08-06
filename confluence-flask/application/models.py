from . import db
class Influencers(db.Model):
    __tablename__ = 'influencers'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False)
    Fname = db.Column(db.String(100), nullable=False)
    Mname = db.Column(db.String(100), nullable=True)
    Lname = db.Column(db.String(100), nullable=True)
    gender = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    socialmedia = db.Column(db.String(100), nullable=False)
    profilePic = db.Column(db.String, nullable=True)
    password = db.Column(db.String(100), nullable=False)
    # Define backref here
    accounts = db.relationship('InfluencerAccounts', backref='influencer', cascade="all, delete-orphan")

class InfluencerAccounts(db.Model):
    __tablename__ = 'Influencer_accounts'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    influencer_id = db.Column(db.Integer, db.ForeignKey('influencers.id'), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    # Do not define backref here
    
class Sponsors(db.Model):
    __tablename__ = 'sponsors'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    website = db.Column(db.String(100), nullable=False)
