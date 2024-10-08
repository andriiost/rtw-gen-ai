from flask import Flask
from .config import config
from flask_cors import CORS
from dotenv import load_dotenv
from .extensions import db, ma, migrate
from .routes.accommodation_routes import accommodation_routes
from .routes.document_routes import document_routes

def create_app(config_mode):
    """
    Create a Flask application instance with a specified configuration.

    This function sets up the application, including loading environment variables,
    initializing extensions such as SQLAlchemy, Marshmallow, and Flask-Migrate, 
    and registering the necessary blueprints (routes).

    :param config_mode: The configuration mode (e.g., 'development', 'production') as specified in the config.py file.
    :return: Configured Flask application instance.
    """
    # Load environment variables
    load_dotenv()

    # Create Flask application
    app = Flask(__name__)
    CORS(app)

    # Load app configuration based on the mode (development/production)
    app.config.from_object(config[config_mode])

    # Initialize extensions with app
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints for accommodation and document routes
    app.register_blueprint(accommodation_routes)
    app.register_blueprint(document_routes)

    return app
