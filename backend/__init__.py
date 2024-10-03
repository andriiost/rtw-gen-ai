from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from .config import config

# Initialize extensions
db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()

def create_app(config_mode):
    # Create Flask application
    app = Flask(__name__)

    # Set config
    app.config.from_object(config[config_mode])

    # Initialize extensions with app
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)

    # Import and register blueprints
    from .routes import accommodation_routes
    app.register_blueprint(accommodation_routes)

    return app
