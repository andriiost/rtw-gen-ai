from flask import Blueprint, jsonify, request
from .models import Accommodation, Industry, InjuryLocation
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
# Multiple Accommodations Route with Sorting and Filtering using GET query parameters
@accommodation_routes.route('/accommodations', methods=['GET'])
def get_accommodations():
    # Get pagination and sorting from query parameters
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 20, type=int)
    sort_by = request.args.get('sort_by', 'accommodation_id')  # Default sort by id
    sort_order = request.args.get('sort_order', 'asc')  # Default is ascending order
    offset = (page - 1) * limit

    # Extract list-based filters from query parameters
    industry_ids = request.args.get('industry_ids', '')
    injury_location_ids = request.args.get('injury_location_ids', '')
    verified = request.args.get('verified', None)

    # Convert comma-separated strings to lists of integers
    if industry_ids:
        industry_ids = [int(i) for i in industry_ids.split(',')]
    if injury_location_ids:
        injury_location_ids = [int(i) for i in injury_location_ids.split(',')]

    # Convert 'verified' parameter to boolean if provided
    if verified is not None:
        verified = verified.lower() in ['true', '1']

    # Map sort_by fields to model attributes
    sort_by_column_map = {
        'accommodation_id': Accommodation.accommodation_id,
        'name': Accommodation.accommodation_name
    }

    # Ensure we have a valid sorting column
    sort_column = sort_by_column_map.get(sort_by, Accommodation.accommodation_id)

    # Apply sorting based on sort_order
    sort_criteria = asc(sort_column) if sort_order == 'asc' else desc(sort_column)

    # Base query for accommodations
    query = db.session.query(Accommodation)\
        .options(
            selectinload(Accommodation.document),
            selectinload(Accommodation.industries),
            selectinload(Accommodation.injury_natures),
            selectinload(Accommodation.injury_locations)
        )

    # Apply filters if provided in the query parameters
    if industry_ids:
        query = query.join(Accommodation.industries).filter(Industry.industry_id.in_(industry_ids))
    if injury_location_ids:
        query = query.join(Accommodation.injury_locations).filter(InjuryLocation.injury_location_id.in_(injury_location_ids))
    if verified is not None:
        query = query.filter(Accommodation.verified == verified)

    # Apply sorting and pagination
    accommodations = query.order_by(sort_criteria)\
        .offset(offset)\
        .limit(limit)\
        .all()

    # Serialize the results
    schema = AccommodationSchema(many=True)
    result = schema.dump(accommodations)

    # Return the results with pagination, sorting, and filtering metadata
    return jsonify({
        'accommodations': result,
        'page': page,
        'limit': limit,
        'sort_by': sort_by,
        'sort_order': sort_order,
        'industry_ids': industry_ids,
        'injury_location_ids': injury_location_ids,
        'verified': verified
    })
