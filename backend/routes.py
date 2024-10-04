from flask import Blueprint, jsonify, request
from .models import Accommodation, Industry, InjuryLocation, InjuryNature, Document
from .schemas import AccommodationSchema
from sqlalchemy.orm import selectinload
from sqlalchemy import asc, desc
from . import db
from datetime import datetime

# Create a blueprint
accommodation_routes = Blueprint('accommodation_routes', __name__)

# Helper function for standardized error handling
def handle_error(message, status_code=400):
    return jsonify({"success": False, "message": message, "data": None}), status_code

# Helper function for standardized success handling
def handle_success(message, data=None, status_code=200):
    return jsonify({"success": True, "message": message, "data": data}), status_code

# Single Accommodation
@accommodation_routes.route('/accommodations/<int:id>', methods=['GET'])
def get_accommodation(id):
    try:
        accommodation = db.session.query(Accommodation)\
            .options(
                selectinload(Accommodation.document),
                selectinload(Accommodation.industries),
                selectinload(Accommodation.injury_natures),
                selectinload(Accommodation.injury_locations)
            ).filter_by(accommodation_id=id).first()

        if not accommodation:
            return handle_error("Accommodation not found", 404)

        schema = AccommodationSchema()
        result = schema.dump(accommodation)

        # Return the accommodation details
        return handle_success("Accommodation retrieved successfully", result)

    except Exception as e:
        # Handle unexpected errors
        return handle_error(f"An error occurred: {str(e)}", 500)

# Multiple Accommodations Route with Sorting and Filtering using GET query parameters
@accommodation_routes.route('/accommodations', methods=['GET'])
def get_accommodations():
    try:
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
        return handle_success("Accommodations retrieved successfully", {
            'accommodations': result,
            'page': page,
            'limit': limit,
            'sort_by': sort_by,
            'sort_order': sort_order,
            'industry_ids': industry_ids,
            'injury_location_ids': injury_location_ids,
            'verified': verified
        })

    except Exception as e:
        # Handle unexpected errors
        return handle_error(f"An error occurred: {str(e)}", 500)

# Update Accommodation
@accommodation_routes.route('/accommodations/<int:accommodation_id>', methods=['PUT'])
def update_accommodation(accommodation_id):
    try:
        # Step 1: fetch the existing accommodation by ID
        accommodation = db.session.query(Accommodation)\
            .options(
                selectinload(Accommodation.document),
                selectinload(Accommodation.industries),
                selectinload(Accommodation.injury_locations),
                selectinload(Accommodation.injury_natures)
            ).filter_by(accommodation_id=accommodation_id).first()

        if not accommodation:
            return handle_error("Accommodation not found", 404)

        # Step 2: Get the request body data
        data = request.get_json()

        if not data:
            return handle_error("Invalid request body", 400)

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
                return handle_error("Invalid date format. Use YYYY-MM-DD", 400)

        # Handle the document URL if passed
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
                    return handle_error(f"Industry '{industry_name}' not found", 400)

        # Injury Locations
        if 'injury_locations' in data:
            accommodation.injury_locations.clear()  # Clear existing relationships
            for location_name in data['injury_locations']:
                injury_location = db.session.query(InjuryLocation).filter_by(injury_location_name=location_name).first()
                if injury_location:
                    accommodation.injury_locations.append(injury_location)
                else:
                    return handle_error(f"Injury Location '{location_name}' not found", 400)

        # Injury Natures
        if 'injury_natures' in data:
            accommodation.injury_natures.clear()  # Clear existing relationships
            for nature_name in data['injury_natures']:
                injury_nature = db.session.query(InjuryNature).filter_by(injury_nature_name=nature_name).first()
                if injury_nature:
                    accommodation.injury_natures.append(injury_nature)
                else:
                    return handle_error(f"Injury Nature '{nature_name}' not found", 400)

        # Step 5: Save changes to database
        db.session.commit()

        # Step 6: Prepare the updated response
        schema = AccommodationSchema()
        result = schema.dump(accommodation)

        # Step 7: Return the response
        return handle_success("Accommodation updated successfully", result)

    except Exception as e:
        # Handle unexpected errors
        return handle_error(f"An error occurred: {str(e)}", 500)

# Delete Accommodation
@accommodation_routes.route('/accommodations/<int:accommodation_id>', methods=['DELETE'])
def delete_accommodation(accommodation_id):
    try:
        # Step 1: Fetch the accommodation by ID
        accommodation = db.session.query(Accommodation).filter_by(accommodation_id=accommodation_id).first()

        if not accommodation:
            return handle_error("Accommodation not found", 404)

        # Step 2: Delete the accommodation
        db.session.delete(accommodation)
        db.session.commit()

        # Step 3: Return success response
        return handle_success("Accommodation deleted successfully", {"accommodation_id": accommodation_id})

    except Exception as e:
        # Step 4: Handle unexpected errors
        return handle_error(f"An error occurred during the deletion process: {str(e)}", 500)
