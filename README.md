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

`Demo practice` is the folder that i have done my flask learning work, i will implement all my knowledge from that concepts and polish them to make a full fledged application.

# Steps of installation

1. Fork the repository and then clone the repository in your local machine
2. go to `/confluence-venv/bin/` and run `activate` to activate the virtual environment

if any error occurs then run the following command
create a virtual environment
and install the dependencies
- flask
- sqlalchemy
- flask_sqlalchemy

3. cd to `confluence-flask`
4. run `python app.py` to start the server
5. open the browser and go to `http://http://127.0.0.1:5000/`

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
1. Accepting and rejecting sponsorships
2. application management
3. Mail system
4. admin portal