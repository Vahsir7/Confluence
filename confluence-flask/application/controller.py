from flask import request, render_template, Blueprint, redirect, url_for, flash
from .models import *
from . import db
import os

main_bp = Blueprint('main', __name__)


#landing home page
@main_bp.route('/')
def signin():
    '''
    This function renders the signin page
    '''
    return render_template('signin.html')
    #return redirect('/login')


#login page 
#give details and enter
#checks from influencerAccounts db
@main_bp.route('/login', methods=['GET'])
def login():
    email = request.args.get('email')
    password = request.args.get('password')
    logintype = request.args.get('type')
    
    if logintype == 'influencer':
        if '@' in email:
            influencer = InfluencerAccounts.query.filter_by(email=email, password=password).first()
        else:
            influencer = InfluencerAccounts.query.filter_by(username=email, password=password).first()
        #print("*************************")
        #print(email,password,type)
        #print(influencer)
        if influencer:
            #print("rendering influencer dashboard")
            #influencer = Influencers.query.filter_by(id=influencer.influencer_id).first()
            return redirect(f'/influencer/{influencer.username}')
        
        return render_template('signin.html', error='Invalid email or password')
    
    elif logintype == 'sponsor':
        sponsor = Sponsors.query.filter_by(email=email, password=password).first()
        if sponsor:
            return render_template('sponsor_dashboard.html', sponsor=sponsor)
        return render_template('signin.html', error='Invalid email or password')
    else:
        return render_template('Welcome admin')
    
#redirects to either signup_influencer or signup_sponsor
@main_bp.route('/signup')
def signup_type():
    return render_template('signup_option.html')

#signup page for influencer
#enter details and submit
#details are stored in influencer db
@main_bp.route('/signup/influencer',methods=['POST','GET'])
def signup_influencer():
    if request.method == 'POST':
        Fname = request.form['Fname']
        Mname = request.form['Mname']
        Lname = request.form['Lname']
        username = request.form['username']
        gender = request.form['gender']
        phone = request.form['phone']
        address = request.form['address']
        email = request.form['email']
        socialmedia = request.form['socialmedia']
        password = request.form['password']
        profilePic = request.files['profilePic']

        if (username in [influencer.username for influencer in Influencers.query.all()]) :
            return render_template('signup_influencer.html', error='Username already exists',
                                   Fname=Fname, Mname=Mname, Lname=Lname, username=username,
                                   gender=gender, phone=phone, address=address, email=email,
                                   socialmedia=socialmedia)
        
        elif (email in [influencer.email for influencer in Influencers.query.all()]):
            return render_template('signup_influencer.html', error='Email already exists'
                                   ,Fname=Fname, Mname=Mname, Lname=Lname, username=username,
                                   gender=gender, phone=phone, address=address, email=email,
                                   socialmedia=socialmedia)

        else:
            if profilePic.filename != '':
                filename = username
            else:
                if gender == 'male':
                    filename = 'male'
                elif gender == 'female':
                    filename = 'female'
                else:
                    filename = 'neutral'
            filename += '.jpg'
            profilePic.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static/uploads', filename))

            influencer = Influencers(Fname=Fname,Mname=Mname,Lname=Lname,username=username,gender=gender,phone=phone,address=address,email=email,socialmedia=socialmedia,password=password,profilePic=filename)
            account = InfluencerAccounts(email=email,username=username,password=password,influencer=influencer)
            db.session.add(account)
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

# influencer dashboard
@main_bp.route('/influencer/<username>')
def influencer_dashboard(username):
    influencer = Influencers.query.filter_by(username=username).first()
    return render_template('influencer_dashboard.html', influencer=influencer)

#infleuncer profile
@main_bp.route('/influencer/<username>/profile')
def influencer_profile(username):
    influencer = Influencers.query.filter_by(username=username).first()
    return render_template('influencer_profile.html', influencer=influencer)

@main_bp.route('/influencer/<username>/update', methods=['POST'])
def influencer_update(username):
    influencer = Influencers.query.filter_by(username=username).first()
    filename = influencer.profilePic
    email = influencer.email
    if request.method == 'POST':
        #return request.form
        Fname = request.form['Fname']
        Mname = request.form['Mname']
        Lname = request.form['Lname']
        newusername = request.form['username']
        gender = request.form['gender']
        phone = request.form['phone']
        address = request.form['address']
        newemail = request.form['email']
        socialmedia = request.form['socialmedia']
        password = request.form['password']
        profilePic = request.files['profilePic']

        if (newusername in [influencer.username for influencer in Influencers.query.all()]) :
            if(newusername != username):
                #print('Username already exists')
                return render_template('influencer_profile.html', influencer=influencer, error='Username already exists')
        
        if (newemail in [influencer.email for influencer in Influencers.query.all()]):
            if(newemail != email):
                print('Email already exists')
                return render_template('influencer_profile.html', influencer=influencer, error='Email already exists')
        
        if profilePic.filename != '':
            filename = username
            profilePic.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static/uploads', filename))

        
        db.session.query(Influencers).filter(Influencers.username == username).update({
            Influencers.Fname: Fname,
            Influencers.Mname: Mname,
            Influencers.Lname: Lname,
            Influencers.gender: gender,
            Influencers.username: newusername,
            Influencers.phone: phone,
            Influencers.address: address,
            Influencers.email: newemail,
            Influencers.socialmedia: socialmedia,
            Influencers.password: password,
            Influencers.profilePic: filename
        })
        db.session.commit()
        return redirect(f'/influencer/{newusername}/profile')
    return redirect(f'/influencer/{username}/profile')