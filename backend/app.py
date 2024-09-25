from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate

# Initialize extensions
db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()

def create_app():
    # Create Flask application
    app = Flask(__name__)

    # Set config
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://azureuser:Accommodations2024@rtw-accommodations.database.windows.net:1433/rtw-accommodations?driver=ODBC+Driver+18+for+SQL+Server'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = True
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_size': 10,            # Number of persistent connections in the pool
    'max_overflow': 20,         # Max connections allowed to overflow
    'pool_recycle': 1800,       # Recycle connections every 30 minutes
    'pool_timeout': 30          # Timeout before giving up on acquiring a connection
}


    # Initialize extensions with app
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)

    # Import and register blueprints
    from routes import accommodation_routes
    app.register_blueprint(accommodation_routes)

    return app
