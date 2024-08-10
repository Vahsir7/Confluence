from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = 'application/static/uploads'
    app.config['SECRET_KEY'] = '1234'  

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Import the models and routes to ensure they are registered
    with app.app_context():
        from .models import Influencers, Sponsors, InfluencerAccounts, Applications, Campaigns
        db.create_all()

    # Register the blueprints
    from .controller import main_bp
    app.register_blueprint(main_bp)
    
    login_manager.login_view = 'main.login'

    @login_manager.user_loader
    def load_user(user_id):
        user = InfluencerAccounts.query.get(user_id)
        if user:
            return user
        return Sponsors.query.get(user_id)



    return app
