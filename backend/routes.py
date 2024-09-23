from flask import Blueprint, jsonify
from models import Accommodation
from schemas import AccommodationSchema
from sqlalchemy.orm import joinedload
from app import db

# Create a blueprint
accommodation_routes = Blueprint('accommodation_routes', __name__)

@accommodation_routes.route('/accommodations/<int:id>', methods=['GET'])
def get_accommodation(id):
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
    schema = AccommodationSchema()
    result = schema.dump(accommodation)
    
    return jsonify(result)
