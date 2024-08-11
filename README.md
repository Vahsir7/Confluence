# Confluence
Influencer Engagement and Sponsorship Coordination Platform. 

This is a web application that connects influencers and sponsors. Influencers can register and login to view all the campaigns and sponsors can register and login to add new campaigns.
The influencers will receive payment after each campaign is completed.
There will be a admin portal that can manage all the campaigns and users.

# Tech Stack
1. Flask
2. SQLAlchemy
3. SQLite
4. HTML
5. CSS
6. Bootstrap
7. Javascript (only for some visual effects)


# Steps of installation

1. Fork the repository and then clone the repository in your local machine
2. create a virtual environment and install the dependencies using the following command
```bash 
pip install -r requirements.txt
```
The following dependencies will be installed
- flask
- sqlalchemy
- flask_sqlalchemy
- flask-migrate
- flask-login

3. run this command to to start the server
```bash
python app.py
``` 

4. open the browser and go to `http://127.0.0.1:5000/`

# Features

## Influencer
1. User can register and login
2. If you are using it for the first click signup
3. login with your details
4. go to profile to update or delete account
5. view all the campaigns from `Search` option

## Sponsors
1. Company can register and login
2. If you are using it for the first click signup
3. login with your details
4. go to profile to update or delete account
5. Add new campaigns from the `Add Campaign` option

# WIP
1. Mail system
2. admin portal
3. aesthetical changes
4. add filters in search panel
5. Additional features such as rating system
