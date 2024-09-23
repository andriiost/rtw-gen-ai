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

    # Initialize extensions with app
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)

    # Import and register blueprints
    from routes import accommodation_routes
    app.register_blueprint(accommodation_routes)

    return app
