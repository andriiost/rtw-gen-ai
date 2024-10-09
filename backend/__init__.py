from flask import Flask
from .config import config
from flask_cors import CORS
from dotenv import load_dotenv
from .extensions import db, ma, migrate
from .routes.accommodation_routes import accommodation_routes
from .routes.document_routes import document_routes
import os

# Required environment variables
REQUIRED_ENV_VARS = [
    "AZURE_OPENAI_API_KEY",
    "AZURE_OPENAI_ENDPOINT",
    "OPENAI_API_VERSION",
    "AZURE_OPENAI_DEPLOYMENT_NAME",
    "AZURE_STORAGE_ACCOUNT",
    "AZURE_BLOB_KEY",
    "AZURE_BLOB_CONTAINER",
    "OPENAI_API_VERSION",
    "DEVELOPMENT_DATABASE_URL"
]

def check_env_vars(required_vars):
    """
    Check if all required environment variables are set.
    """
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        error_message = f"Missing environment variables: {', '.join(missing_vars)}"
        raise EnvironmentError(error_message)


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

    # Check environment variables before initializing the app
    check_env_vars(REQUIRED_ENV_VARS)

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
