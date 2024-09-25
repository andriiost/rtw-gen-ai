from flask import Blueprint, jsonify, request
from models import Accommodation
from schemas import AccommodationSchema
from sqlalchemy.orm import selectinload, load_only
from app import db

# Create a blueprint
accommodation_routes = Blueprint('accommodation_routes', __name__)

# Single Accommodation
@accommodation_routes.route('/accommodations/<int:id>', methods=['GET'])
def get_accommodation(id):
    accommodation = db.session.query(Accommodation)\
        .options(
            selectinload(Accommodation.document),
            selectinload(Accommodation.industries),
            selectinload(Accommodation.injury_natures),
            selectinload(Accommodation.injury_locations)
        ).filter_by(accommodation_id=id).first()

    if not accommodation:
        return jsonify({"message": "Accommodation not found"}), 404
    
    schema = AccommodationSchema()
    result = schema.dump(accommodation)
    
    return jsonify(result)


# Multiple Accommodations
@accommodation_routes.route('/accommodations', methods=['GET'])
def get_accommodations():
    # Get the page number and the number of items per page from query parameters
    page = request.args.get('page', 1, type=int)  # default to page 1
    per_page = request.args.get('per_page', 10, type=int)  # default to 10 items per page
    
    # Calculate the offset for pagination
    offset = (page - 1) * per_page
    
    # Query the database with an order by and limit using OFFSET and FETCH for MSSQL
    paginated_accommodations = db.session.query(Accommodation)\
        .order_by(Accommodation.accommodation_id.asc())\
        .offset(offset)\
        .limit(per_page)\
        .all()
    
    schema = AccommodationSchema(many=True)
    
    # Serialize the paginated items
    result = schema.dump(paginated_accommodations)
    
    # Return the paginated result along with pagination metadata
    return jsonify({
        'accommodations': result,
        'page': page,
        'per_page': per_page
    })
