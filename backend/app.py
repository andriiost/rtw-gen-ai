from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from models import Accommodation, AccommodationSchema
from sqlalchemy.orm import joinedload

#init app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://azureuser:Accommodations2024@rtw-accommodations.database.windows.net:1433/rtw-accommodations?driver=ODBC+Driver+18+for+SQL+Server'

#init db
db = SQLAlchemy(app)

#init ma
ma = Marshmallow(app)

# API endpoint to get accommodation by ID
@app.route('/accommodations/<int:id>', methods=['GET'])
def get_accommodation(id):
    # Query the accommodation by id, also loading related tables
    accommodation = db.session.query(Accommodation)\
        .options(
            joinedload(Accommodation.document),
            joinedload(Accommodation.industries),
            joinedload(Accommodation.injury_natures),
            joinedload(Accommodation.injury_locations)
        ).filter_by(accommodation_id=id).first()
    
    if not accommodation:
        return jsonify({"message": "Accommodation not found"}), 404
    
    # Serialize the result using the custom schema
    result = AccommodationSchema(accommodation).__dict__
    
    return jsonify(result)

#run server
if __name__ == "__main__":
    app.run(debug=True)
