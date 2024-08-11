from flask import request, render_template, Blueprint, redirect, url_for, flash, session, abort
from flask_login import login_user, logout_user, login_required, current_user
from .models import *
from functools import wraps
from . import db
from datetime import datetime
import os

main_bp = Blueprint('main', __name__)


def user_required(f):
    @wraps(f)
    
    def decorated_function(*args, **kwargs):

        if request.endpoint == 'main.logout':
            return f(*args, **kwargs)

        #print(current_user)
        #print("args",args)
        #print("kwargs",kwargs)
        username = kwargs.get('username')
        companycode = kwargs.get('companycode')
        #print(f"username : {username} and companycode : {companycode}")
        # Check if current_user is logged in
        if not current_user.is_authenticated:
            return redirect(url_for('main.signin'))
        
        logintype = session.get('logintype')
        
        if (logintype=="influencer" and not username) or (logintype=="sponsor" and not companycode):
            abort(403)
        #print("login type",logintype)
        
        user_id = session.get('user_id')
        if logintype == "sponsor":
            if companycode and current_user.companycode != companycode:
                return redirect(url_for('main.sponsor_dashboard', companycode=current_user.companycode))
        elif logintype == "influencer":
            if username and current_user.username != username:
                return redirect(url_for('main.influencer_dashboard', username=current_user.username))
        else:
            return redirect('/')
        
        return f(*args, **kwargs)
    
    return decorated_function

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
    session['logintype'] = logintype
    if logintype == 'influencer':
        influencer = InfluencerAccounts.query.filter_by(email=email, password=password).first()
        if not influencer:
            influencer = InfluencerAccounts.query.filter_by(username=email, password=password).first()
        if influencer:
            login_user(influencer)
            return redirect(f'/influencer/{influencer.username}')
        return render_template('signin.html', error='Invalid email or password')
    
    elif logintype == 'sponsor':
        sponsor = Sponsors.query.filter_by(email=email, password=password).first()
        if not sponsor:
            sponsor = Sponsors.query.filter_by(companycode=email, password=password).first()
        if sponsor:
            login_user(sponsor)
            return redirect(f'/sponsor/{sponsor.companycode}')
        return render_template('signin.html', error='Invalid email or password')
    elif logintype == 'admin':
        return render_template('Welcome admin')
    else:
        return redirect('/')

#logout
@main_bp.route('/logout')
@login_required
@user_required
def logout():
    print("logging out")
    logout_user()
    return redirect(url_for('main.signin'))


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
        
        if (email in [influencer.email for influencer in Influencers.query.all()]):
            return render_template('signup_influencer.html', error='Email already exists'
                                   ,Fname=Fname, Mname=Mname, Lname=Lname, username=username,
                                   gender=gender, phone=phone, address=address, email=email,
                                   socialmedia=socialmedia)

        if profilePic.filename != '':
            filename = username
            filename += '.jpg'
            profilePic.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), 
                                         'static/uploads/influencers', filename))
        else:
            if gender == 'male':
                filename = 'male.jpg'
            elif gender == 'female':
                filename = 'female.jpg'
            else:
                filename = 'neutral.jpg'

        influencer = Influencers(Fname=Fname,Mname=Mname,Lname=Lname,
                                 username=username,gender=gender,phone=phone,address=address,
                                 email=email,socialmedia=socialmedia,password=password,
                                 profilePic=filename)
        
        account = InfluencerAccounts(email=email,username=username,
                                     password=password,influencer=influencer)
        
        db.session.add(account)
        db.session.add(influencer)
        db.session.commit()

        return render_template('signin.html')
    return render_template('signup_influencer.html')

#signup page for sponsor
@main_bp.route('/signup/sponsor',methods=['POST','GET'])
def signup_sponsor():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        companycode = request.form['companycode']
        password = request.form['password']
        address = request.form['address']
        phone = request.form['phone']
        industry = request.form['industry']
        website = request.form['website']
        companyLogo = request.files['companyLogo']

        if (companycode in [sponsor.companycode for sponsor in Sponsors.query.all()]):
            return render_template('signup_sponsor.html', error='Company code already exists', 
                                   name=name, email=email, companycode=companycode, 
                                   address=address, phone=phone, industry=industry, website=website)
        
        if (email in [sponsor.email for sponsor in Sponsors.query.all()]):
            return render_template('signup_sponsor.html', error='Email already exists', 
                                   name=name, email=email, companycode=companycode, 
                                   address=address, phone=phone, industry=industry, website=website)
        
        if companyLogo.filename != '':
            filename = companycode
            #filename += '.jpg'
            companyLogo.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static/uploads/sponsors', filename))
        else:
            filename = 'defaultCompany.jpg'
        
        sponsor = Sponsors(name=name,
                           email=email,
                           companycode=companycode,
                           address=address,
                           phone=phone,
                           password=password,
                           industry=industry,
                           website=website,
                           companyLogo=filename)
        
        db.session.add(sponsor)
        db.session.commit()
        return render_template('signin.html')
    return render_template('signup_sponsor.html')

# influencer dashboard
@main_bp.route('/influencer/<username>')
@login_required
@user_required
def influencer_dashboard(username):
    influencer = Influencers.query.filter_by(username=username).first()
    applications = Applications.query.filter_by(influencer_id=username).all()
    campaigns = []
    statuses = []
    for application in applications:
        campaign = Campaigns.query.filter_by(id=application.campaign_id).first()
        campaigns.append(campaign)
        statuses.append(application.status)
    return render_template('influencer_dashboard.html', username=username, influencer=influencer, campaigns=campaigns, status=statuses)

#infleuncer profile
@main_bp.route('/influencer/<username>/profile')
@login_required
@user_required
def influencer_profile(username):
    influencer = Influencers.query.filter_by(username=username).first()
    return render_template('influencer_profile.html', influencer=influencer)

@main_bp.route('/influencer/<username>/update', methods=['POST'])
@login_required
@user_required
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
            profilePic.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static/uploads/influencers', filename))

        
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

#delete influencer profile
@main_bp.route('/influencer/<username>/delete',methods=['GET','POST'])
@login_required
@user_required
def influencer_delete(username):
    if request.method == 'POST':
        password = request.form['password']
        influencer = Influencers.query.filter_by(username=username).first()
        userpassword = influencer.password
        print(password)
        print(userpassword)
        if(password == userpassword):
            db.session.delete(influencer)
            db.session.commit()
        else:
            print('Invalid password')
            return render_template('influencer_delete.html', username=username,error='Invalid password')
        return redirect('/')
    return render_template('influencer_delete.html', username=username)

#view campaigns
@main_bp.route('/influencer/<username>/campaigns')
@login_required
@user_required
def influencer_campaigns(username):
    campaigns = Campaigns.query.all()
    #print(len(campaigns))
    return render_template('campaigns_list.html', username=username, campaigns=campaigns)

#view campaign details
@main_bp.route('/influencer/<username>/campaigns/<int:id>')
@login_required
@user_required
def influencer_campaign_details(username, id):
    campaign = Campaigns.query.filter_by(id=id).first()
    application = Applications.query.filter_by(influencer_id=username, campaign_id=id).first()
    print(application)
    if not application:
        status = 'NA'
    else:
        status = application.status

    return render_template('campaign_details.html',username=username, campaign=campaign, status=status)

#apply from influencer
@main_bp.route('/influencer/<username>/campaigns/<int:id>/apply')
@login_required
@user_required
def apply_campaign(username, id):
    influencer = Influencers.query.filter_by(username=username).first()
    campaign = Campaigns.query.filter_by(id=id).first()
    sponsor = Sponsors.query.filter_by(companycode=campaign.sponsor_id).first()
    # create application
    application = Applications.query.filter_by(influencer_id=username, campaign_id=id).first()
    if not application:
        print("creating application")
        application = Applications(influencer_id=username, campaign_id=id, sponsor_id=campaign.sponsor_id, status='PENDING')
        print(application)

        campaign.totalApplications += 1
        Campaigns.query.filter_by(id=id).update({'totalApplications': campaign.totalApplications})

        db.session.add(application)
        db.session.commit()
    return redirect(f'/influencer/{username}/campaigns/{id}')


    

#sponsor dashboard
@main_bp.route('/sponsor/<companycode>')
@login_required
@user_required
def sponsor_dashboard(companycode):
    sponsor = Sponsors.query.filter_by(companycode=companycode).first()
    campaigns = Campaigns.query.filter_by(sponsor_id=sponsor.companycode).all()
    print(campaigns)
    return render_template('sponsor_dashboard.html', sponsor=sponsor, campaigns=campaigns)

#sponsor profile
@main_bp.route('/sponsor/<companycode>/profile')
@login_required
@user_required
def sponsor_profile(companycode):
    sponsor = Sponsors.query.filter_by(companycode=companycode).first()
    return render_template('sponsor_profile.html', sponsor=sponsor)

#update sponsor profile
@main_bp.route('/sponsor/<companycode>/update', methods=['POST'])
@login_required
@user_required
def sponsor_update(companycode):
    sponsor = Sponsors.query.filter_by(companycode=companycode).first()
    filename = sponsor.companyLogo
    email = sponsor.email
    if request.method == 'POST':
        name = request.form['name']
        newemail = request.form['email']
        newcompanycode = request.form['companycode']
        password = request.form['password']
        address = request.form['address']
        phone = request.form['phone']
        industry = request.form['industry']
        website = request.form['website']
        companyLogo = request.files['companyLogo']

        if (newcompanycode in [sponsor.companycode for sponsor in Sponsors.query.all()]):
            if(newcompanycode != companycode):
                return render_template('sponsor_profile.html', sponsor=sponsor, error='Company code already exists')
        
        if (newemail in [sponsor.email for sponsor in Sponsors.query.all()]):
            if(newemail != email):
                return render_template('sponsor_profile.html', sponsor=sponsor, error='Email already exists')
        
        if companyLogo.filename != '':
            filename = companycode
            companyLogo.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static/uploads/sponsors', filename))

        db.session.query(Sponsors).filter(Sponsors.companycode == companycode).update({
            Sponsors.name: name,
            Sponsors.email: newemail,
            Sponsors.companycode: newcompanycode,
            Sponsors.password: password,
            Sponsors.address: address,
            Sponsors.phone: phone,
            Sponsors.industry: industry,
            Sponsors.website: website,
            Sponsors.companyLogo: filename
        })
        db.session.commit()
        return redirect(f'/sponsor/{newcompanycode}/profile')
    return redirect(f'/sponsor/{companycode}/profile')

#delete sponsor profile
@main_bp.route('/sponsor/<companycode>/delete',methods=['GET','POST'])
@login_required
@user_required
def sponsor_delete(companycode):
    if request.method == 'POST':
        password = request.form['password']
        sponsor = Sponsors.query.filter_by(companycode=companycode).first()
        userpassword = sponsor.password
        if(password == userpassword):
            db.session.delete(sponsor)
            db.session.commit()
        else:
            return render_template('sponsor_delete.html', companycode=companycode,error='Invalid password')
        return redirect('/')
    return render_template('sponsor_delete.html', companycode=companycode)

# add campaign
@main_bp.route('/sponsor/<companycode>/campaign/create', methods=['POST','GET'])
@login_required
@user_required
def create_campaign(companycode):

    sponsor = Sponsors.query.filter_by(companycode=companycode).first()
    campaign = Campaigns.query.filter_by(sponsor_id=companycode).first()

    if request.method == 'POST':
        Title = request.form['Title']
        Description = request.form['Description']
        tags = request.form['tags']
        Salary = request.form['Salary']
        videos_req = request.form['videos_req']
        StartDate = datetime.strptime(request.form['StartDate'], '%Y-%m-%d').date()
        EndDate = datetime.strptime(request.form['EndDate'], '%Y-%m-%d').date()

        contact_phone = sponsor.phone
        contact_email = sponsor.email
        companyLogo = sponsor.companyLogo
        companyName = sponsor.name

        campaign = Campaigns(sponsor_id=companycode,
                             companyLogo=companyLogo,
                             companyName=companyName,
                             Title=Title,
                             Description=Description,
                             tags=tags,
                             Salary=Salary,
                             videos_req=videos_req,
                             StartDate=StartDate,
                             EndDate=EndDate,
                             contact_phone=contact_phone,
                             contact_email=contact_email)
        
        db.session.add(campaign)
        db.session.commit()
        return redirect(f'/sponsor/{companycode}')
    
    print(sponsor.companycode)
    return render_template('campaign_add.html', sponsor=sponsor, campaign=campaign)

#view campaigns
@main_bp.route('/sponsor/<companycode>/campaigns')
@login_required
@user_required
def display_campaigns(companycode):
    campaigns = Campaigns.query.filter_by(sponsor_id=companycode).all()
    return render_template('sponsor_campaigns_list.html', companycode=companycode, campaigns=campaigns)

#view campaign details
@main_bp.route('/sponsor/<companycode>/campaigns/<int:id>')
@login_required
@user_required
def display_campaign_details(companycode, id):
    campaign = Campaigns.query.filter_by(id=id).first()
    applications = Applications.query.filter_by(campaign_id=id, status="PENDING").all()
    influencers = []
    for application in applications:
        influencer = Influencers.query.filter_by(username=application.influencer_id).first()
        influencers.append(influencer)
    

    accepted_applications = Applications.query.filter_by(campaign_id=id, status="ACCEPTED").all()
    accepted_influencers = []
    for application in accepted_applications:
        influencer = Influencers.query.filter_by(username=application.influencer_id).first()
        accepted_influencers.append(influencer)

    return render_template('sponsor_campaign_details.html',influencers=influencers, companycode=companycode, campaign=campaign, applications=applications, accepted_influencers=accepted_influencers)

#status of application by Sponsor
@main_bp.route('/sponsor/<companycode>/campaigns/<int:id>/status', methods=['POST'])
@login_required
@user_required
def change_application_status(companycode, id):
    influencer_id = request.form['username']
    status = request.form['status']
    #application = Applications.query.filter_by(influencer_id=influencer_id, campaign_id=id).first()
    db.session.query(Applications).filter(Applications.influencer_id == influencer_id, Applications.campaign_id == id).update({
        Applications.status: status
    })
    
    campaign = Campaigns.query.filter_by(id=id).first()
    campaign.totalApplications -= 1
    Campaigns.query.filter_by(id=id).update({'totalApplications': campaign.totalApplications})

    db.session.commit()
    return redirect(f'/sponsor/{companycode}/campaigns/{id}')

