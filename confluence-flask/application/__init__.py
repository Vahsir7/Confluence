from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = 'application/static/uploads'
    
    db.init_app(app)
    

    with app.app_context():
        from .models import Influencers, Sponsors
        db.create_all()
    
    # Import the routes to ensure they are registered
    from .controller import main_bp
    app.register_blueprint(main_bp)
    
    return app
