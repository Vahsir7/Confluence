from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = 'application/static/uploads'
    
    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        from .models import Influencers, Sponsors, Campaigns, InfluencerAccounts, Applications
        db.create_all()
    
    # Import the routes to ensure they are registered
    from .controller import main_bp
    app.register_blueprint(main_bp)
    
    return app
