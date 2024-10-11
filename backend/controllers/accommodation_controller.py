from flask import request
from sqlalchemy.orm import selectinload
from sqlalchemy import asc, desc
from ..extensions import db
from ..models import Accommodation, InjuryLocation, Industry, Document, InjuryNature
from ..schemas import AccommodationSchema
from ..helpers.response_helpers import handle_error, handle_success
from datetime import datetime

def get_accommodation(id):
    """
    Retrieve an accommodation by its ID.

    This function fetches an accommodation from the database based on the provided ID.
    It uses SQLAlchemy's `selectinload` to eagerly load related industries, injury locations, and natures
    to optimize performance.

    :param id: The ID of the accommodation to retrieve.
    :return: A JSON response with the accommodation details or an error message.
    """
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

    except ValueError as e:
        # Handle input validation errors
        return handle_error(f"Invalid input: {str(e)}", 400)
    except Exception as e:
        print(f"Unexpected error: {str(e)}")  # In production, use a logger
        return handle_error("An internal server error occurred", 500)
    
def get_accommodations():
    """
    Retrieve a list of accommodations, with optional filtering, sorting, and pagination.

    This function retrieves accommodations from the database, allowing for filtering by industries,
    injury locations, and verification status. It supports pagination and sorting by specified fields.

    Query Parameters:
        - page: The page number for pagination (default: 1).
        - limit: The number of accommodations per page (default: 20).
        - sort_by: The field to sort by (default: 'accommodation_id').
        - sort_order: The sort order ('asc' for ascending, 'desc' for descending).
        - industry_ids: Comma-separated list of industry IDs to filter by.
        - injury_location_ids: Comma-separated list of injury location IDs to filter by.
        - verified: Filter by verification status ('true' or 'false').

    :return: JSON response with a paginated list of accommodations and metadata, or an error message.
    """
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

        # Get total count for pagination
        total_count = query.count()

        # Apply sorting and pagination
        accommodations = query.order_by(sort_criteria)\
            .offset(offset)\
            .limit(limit)\
            .all()

        # Serialize the results
        schema = AccommodationSchema(many=True)
        result = schema.dump(accommodations)

        # Calculate pagination metadata
        total_pages = (total_count + limit - 1) // limit  # ceil-like calculation
        has_next_page = page < total_pages
        has_prev_page = page > 1

        # Return the results with accommodations, pagination, and filters metadata
        return handle_success("Accommodations retrieved successfully", {
            'accommodations': result,
            'pagination': {
                'page': page,
                'limit': limit,
                'total_pages': total_pages,
                'total_items': total_count,
                'has_next_page': has_next_page,
                'has_prev_page': has_prev_page
            },
            'filters': {
                'sort_by': sort_by,
                'sort_order': sort_order,
                'industry_ids': industry_ids,
                'injury_location_ids': injury_location_ids,
                'verified': verified
            }
        })

    except ValueError as e:
        # Handle input validation errors
        return handle_error(f"Invalid input: {str(e)}", 400)
    except Exception as e:
        print(f"Unexpected error: {str(e)}")  # In production, use a logger
        return handle_error("An internal server error occurred", 500)
    
def update_accommodation(accommodation_id):
    """
    Update an accommodation based on the provided ID.

    This function updates an existing accommodation with new data from the request body, 
    including the name, description, verification status, associated document, industries,
    injury locations, and injury natures. It handles many-to-many relationships and date validation.

    Request Body Example:
    ```
    {
      "accommodation_name": "Cooling Vest",
      "accommodation_description": "A cooling vest with ice packs for heat stress relief.",
      "verified": true,
      "date_created": "2024-10-10",
      "document_id": 123,             # ID of the document to link
      "industries": [1, 5],           # List of industry IDs
      "injury_locations": [3, 7],     # List of injury location IDs
      "injury_natures": [10]          # List of injury nature IDs
    }
    ```
    :param accommodation_id: The ID of the accommodation to update.
    :return: JSON response with the updated accommodation details or an error message.
    """
    try:
        accommodation = db.session.query(Accommodation).filter_by(accommodation_id=accommodation_id).first()

        if not accommodation:
            return handle_error("Accommodation not found", 404)

        data = request.get_json()

        if not data:
            return handle_error("Invalid request body", 400)

        accommodation.accommodation_name = data.get('accommodation_name', accommodation.accommodation_name)
        accommodation.accommodation_description = data.get('accommodation_description', accommodation.accommodation_description)
        accommodation.verified = data.get('verified', accommodation.verified)

        date_created = data.get('date_created')
        if date_created:
            try:
                accommodation.date_created = datetime.strptime(date_created, "%Y-%m-%d")
            except ValueError:
                return handle_error("Invalid date format. Use YYYY-MM-DD", 400)

        # Handle Document
        if 'document_id' in data:
            document = db.session.query(Document).filter_by(document_id=data['document_id']).first()
            if document:
                accommodation.document = document
            else:
                return handle_error("Document not found", 404)

        # Update Many-to-Many Relationships with Existing Entities
        if 'industries' in data:
            accommodation.industries.clear()  # Clear existing relationships
            for industry_id in data['industries']:
                industry = db.session.query(Industry).filter_by(industry_id=industry_id).first()
                if industry:
                    accommodation.industries.append(industry)
                else:
                    return handle_error(f"Industry ID '{industry_id}' not found", 400)

        if 'injury_locations' in data:
            accommodation.injury_locations.clear()  # Clear existing relationships
            for location_id in data['injury_locations']:
                injury_location = db.session.query(InjuryLocation).filter_by(injury_location_id=location_id).first()
                if injury_location:
                    accommodation.injury_locations.append(injury_location)
                else:
                    return handle_error(f"Injury Location ID '{location_id}' not found", 400)

        if 'injury_natures' in data:
            accommodation.injury_natures.clear()  # Clear existing relationships
            for nature_id in data['injury_natures']:
                injury_nature = db.session.query(InjuryNature).filter_by(injury_nature_id=nature_id).first()
                if injury_nature:
                    accommodation.injury_natures.append(injury_nature)
                else:
                    return handle_error(f"Injury Nature ID '{nature_id}' not found", 400)

        db.session.commit()

        schema = AccommodationSchema()
        result = schema.dump(accommodation)

        return handle_success("Accommodation updated successfully", result)

    except ValueError as e:
        return handle_error(f"Invalid input: {str(e)}", 400)
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return handle_error("An internal server error occurred", 500)


def delete_accommodation(accommodation_id):
    """
    Delete an accommodation by its ID.

    This function removes an accommodation from the database by its ID.

    :param accommodation_id: The ID of the accommodation to delete.
    :return: JSON response indicating successful deletion or an error message.
    """
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

    except ValueError as e:
        return handle_error(f"Invalid input: {str(e)}", 400)
    except Exception as e:
        print(f"Unexpected error: {str(e)}")  # In production, use a logger
        return handle_error("An internal server error occurred", 500)