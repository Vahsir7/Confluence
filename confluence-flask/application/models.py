from . import db
from flask_login import UserMixin
class Influencers(UserMixin, db.Model):
    __tablename__ = 'influencers'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100),  nullable=False)
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

class InfluencerAccounts(UserMixin, db.Model):
    __tablename__ = 'Influencer_accounts'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    influencer_id = db.Column(db.Integer, db.ForeignKey('influencers.id'), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    # Do not define backref here
    
class Sponsors(UserMixin, db.Model):
    __tablename__ = 'sponsors'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), nullable=False)
    companycode = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    industry = db.Column(db.String(100), nullable=False)
    website = db.Column(db.String(100), nullable=False)
    companyLogo = db.Column(db.String, nullable=True)

    # Define one-to-many relationship with Campaigns
    campaigns = db.relationship('Campaigns', backref='sponsor', cascade="all, delete-orphan")


class Campaigns(UserMixin, db.Model):
    __tablename__ = 'campaigns'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sponsor_id = db.Column(db.Integer, db.ForeignKey('sponsors.id'), nullable=False)
    
    companyLogo = db.Column(db.String, nullable=False)  
    companyName = db.Column(db.String(100), nullable=False)     
    Title = db.Column(db.String(100), nullable=False)
    Description = db.Column(db.String, nullable=False)
    tags = db.Column(db.String, nullable=False)
    Salary = db.Column(db.Float, nullable=False)
    videos_req = db.Column(db.Integer, nullable=True)
    StartDate = db.Column(db.Date, nullable=False)
    EndDate = db.Column(db.Date, nullable=False)
    contact_phone = db.Column(db.String(20), nullable=False)
    contact_email = db.Column(db.String(100), nullable=False)
    totalApplications = db.Column(db.Integer, nullable=False, default=0)

    applications = db.relationship('Applications', backref='campaign', cascade="all, delete-orphan")

class Applications(UserMixin, db.Model):
    __tablename__ = 'applications'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaigns.id'), nullable=False)
    influencer_id = db.Column(db.Integer, db.ForeignKey('influencers.username'), nullable=False)
    sponsor_id = db.Column(db.Integer, db.ForeignKey('sponsors.companycode'), nullable=False)
    status = db.Column(db.String(100), nullable=False)

