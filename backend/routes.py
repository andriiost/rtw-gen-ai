from flask import Blueprint, jsonify, request
from .models import Accommodation
from .schemas import AccommodationSchema
from sqlalchemy.orm import selectinload
from sqlalchemy import asc, desc
from . import db

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

# Multiple Accommodations Route with Sorting
@accommodation_routes.route('/accommodations', methods=['GET'])
def get_accommodations():
    # Get pagination parameters
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 20, type=int)
    offset = (page - 1) * limit

    # Sorting options: sort by 'id' or 'name'
    sort_by = request.args.get('sort_by', 'accommodation_id')  # Default is to sort by 'id'
    sort_order = request.args.get('sort_order', 'asc')  # Default is ascending order

    # Map sort_by fields to model attributes
    sort_by_column_map = {
        'accommodation_id': Accommodation.accommodation_id,
        'name': Accommodation.accommodation_name
    }

    # Ensure we have a valid sorting column
    if sort_by not in sort_by_column_map:
        sort_by = 'accommodation_id'

    # Determine the sorting order (ascending or descending)
    if sort_order == 'asc':
        sort_criteria = asc(sort_by_column_map[sort_by])
    else:
        sort_criteria = desc(sort_by_column_map[sort_by])

    # Fetch accommodations with sorting and pagination
    accommodations = db.session.query(Accommodation)\
        .options(
            selectinload(Accommodation.document),
            selectinload(Accommodation.industries),
            selectinload(Accommodation.injury_natures),
            selectinload(Accommodation.injury_locations)
        )\
        .order_by(sort_criteria)\
        .offset(offset)\
        .limit(limit)\
        .all()

    # Serialize the results
    schema = AccommodationSchema(many=True)
    result = schema.dump(accommodations)

    # Return the results with pagination and sorting metadata
    return jsonify({
        'accommodations': result,
        'page': page,
        'limit': limit,
        'sort_by': sort_by,
        'sort_order': sort_order
    })