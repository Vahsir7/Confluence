from flask import request, render_template, Blueprint, redirect, url_for
from .models import *
from . import db

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def signin():
    '''
    This function renders the signin page
    '''
    return render_template('signin.html')

@main_bp.route('/login')
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    type = request.form.get('type')
    
    if type =='influencer':
        influncer = Influencers.query.filter_by(email=email, password=password).first()
        if influncer:
            return render_template('influencer_dashboard.html',influncer=influncer)
        return render_template('signin.html', error='Invalid email or password')
    
    elif type == 'sponsor':
        sponsor = Sponsors.query.filter_by(email=email, password=password).first()
        if sponsor:
            return render_template('sponsor_dashboard.html',sponsor=sponsor)
        return render_template('signin.html', error='Invalid email or password')
    else:
        return render_template('Welcome admin')
    
@main_bp.route('/signup')
def signup_type():
    return render_template('signup_option.html')

@main_bp.route('/signup/influencer',methods=['POST','GET'])
def signup_influencer():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        account = request.form['account']
        influencer = Influencers(name=name,email=email,password=password,account=account)
        db.session.add(influencer)
        db.session.commit()
        return render_template('signin.html')
    return render_template('signup_influencer.html')

@main_bp.route('/signup/sponsor',methods=['POST','GET'])
def signup_sponsor():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        account = request.form['account']
        sponsor = Sponsors(name=name,email=email,password=password,website=account)
        db.session.add(sponsor)
        db.session.commit()
        return render_template('signin.html')
    return render_template('signup_sponsor.html')