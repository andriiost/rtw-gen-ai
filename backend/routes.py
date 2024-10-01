from flask import Blueprint, jsonify, request
from .models import Accommodation, Industry, InjuryLocation, InjuryNature, Document
from .schemas import AccommodationSchema
from sqlalchemy.orm import selectinload
from sqlalchemy import asc, desc
from . import db
from datetime import datetime

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


# Update Accommodation
@accommodation_routes.route('/accommodation/<int:accommodation_id>', methods=['PUT'])
def update_accommodation(accommodation_id):
    try:
        # Step 1: fetch the existing accommodation by ID
        accommodation = db.session.query(Accommodation)\
            .options(
                selectinload(Accommodation.document),
                selectinload(Accommodation.industries),
                selectinload(Accommodation.injury_locations),
                selectinload(Accommodation.injury_natures)
            ).filter_by(accommodation_id = accommodation_id).first()
        
        if not accommodation:
            return jsonify({"message": "Accommodation not found"}), 404
        
        # Step 2: Get the request body data
        data = request.get_json()
        
        if not data:
            return jsonify({"message": "invalid request body"}), 400
        
        # Step 3: Update the accommodation fields
        accommodation.accommodation_name = data.get('accommodation_name', accommodation.accommodation_name)
        accommodation.accommodation_description = data.get('accommodation_description', accommodation.accommodation_description)
        accommodation.verified = data.get('verified', accommodation.verified)

        # Handle date_created if passed
        date_created = data.get('date_created')
        if date_created:
            try:
                accommodation.date_created = datetime.strptime(date_created, "%Y-%m-%d")
            except ValueError:
                return jsonify({"message": "Invalid date format. Use YYYY-MM-DD"}), 400
            
        # Handle the document url if passed
        if 'url' in data:
            if accommodation.document:
                accommodation.document.url = data['url']
            else:
                # Create a new document entry if it does not exist
                new_document = Document(url=data['url'])
                db.session.add(new_document)
                db.session.commit()
                accommodation.document = new_document

        # Step 4: Update Many-to-Many relationships

        # Industries
        if 'industries' in data:
            accommodation.industries.clear()  # Clear existing relationships
            for industry_name in data['industries']:
                industry = db.session.query(Industry).filter_by(industry_name=industry_name).first()
                if industry:
                    accommodation.industries.append(industry)
                else:
                    return jsonify({"message": f"Industry '{industry_name}' not found"}), 400
                
        # Injury Locations
        if 'injury_locations' in data:
            accommodation.injury_locations.clear()  # Clear existing relationships
            for location_name in data['injury_locations']:
                injury_location = db.session.query(InjuryLocation).filter_by(injury_location_name=location_name).first()
                if injury_location:
                    accommodation.injury_locations.append(injury_location)
                else:
                    return jsonify({"message": f"Injury Location '{location_name}' not found"}), 400

        # Injury Natures
        if 'injury_natures' in data:
            accommodation.injury_natures.clear()  # Clear existing relationships
            for nature_name in data['injury_natures']:
                injury_nature = db.session.query(InjuryNature).filter_by(injury_nature_name=nature_name).first()
                if injury_nature:
                    accommodation.injury_natures.append(injury_nature)
                else:
                    return jsonify({"message": f"Injury Nature '{nature_name}' not found"}), 400

        # Step 5: Save changes to database
        db.session.commit()

        # Step 6: Prepare the updated response
        updated_accommodation = {
            "accommodation_id": accommodation.accommodation_id,
            "accommodation_name": accommodation.accommodation_name,
            "accommodation_description": accommodation.accommodation_description,
            "industries": [industry.industry_name for industry in accommodation.industries],
            "injury_locations": [location.injury_location_name for location in accommodation.injury_locations],
            "injury_natures": [nature.injury_nature_name for nature in accommodation.injury_natures],
            "verified": accommodation.verified,
            "date_created": accommodation.date_created.strftime("%Y-%m-%d") if accommodation.date_created else None,
            "url": accommodation.document.url if accommodation.document else None
        }

        # Step 7: Return the response
        return jsonify({
            "message": "Accommodation updated successfully",
            "accommodation": updated_accommodation
        }), 200
    
    except Exception as e:
        # Handle unexpected errors
        return jsonify({"message": "An error occured", "error": str(e)}), 500
