from flask import Blueprint, jsonify, request
from werkzeug.utils import secure_filename
from .models import Accommodation, Industry, InjuryLocation, InjuryNature, Document
from .schemas import AccommodationSchema
from sqlalchemy.orm import selectinload
from sqlalchemy import asc, desc
from . import db
from datetime import datetime
from azure.storage.blob import BlobServiceClient, ContentSettings
from openai import AzureOpenAI
import os
import fitz
import docx2txt

# Create a blueprint
accommodation_routes = Blueprint('accommodation_routes', __name__)

# Azure Blob Storage setup
blob_service_client = BlobServiceClient(account_url=f"https://{os.getenv('AZURE_STORAGE_ACCOUNT')}.blob.core.windows.net", credential=os.getenv('AZURE_BLOB_KEY'))
container_name = "rtwblobs"

# Azure OpenAI setup
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_version=os.getenv("OPENAI_API_VERSION")
)

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


# Upload Accommodation

# Allowed file extensions
ALLOWED_EXTENSIONS = {'pdf', 'docx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Helper function to extract text based on file type
def extract_text(file_path, extension):
    if extension == 'pdf':
        return extract_text_from_pdf(file_path)
    elif extension == 'docx':
        return extract_text_from_docx(file_path)
    else:
        raise ValueError("Unsupported file type")
    
# Extract text from PDF files
def extract_text_from_pdf(file_path):
    with fitz.open(file_path) as doc:
        text = "\n".join([page.get_text() for page in doc])
    return text

# Extract text from DOCX files
def extract_text_from_docx(file_path):
    return docx2txt.process(file_path)

# Helper function to upload to Azure Blob Storage
def upload_to_blob(file_path, filename, file_extension):
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=filename)
    with open(file_path, "rb") as data:
        blob_client.upload_blob(data, content_settings=ContentSettings(content_type=f"application/{file_extension}"))
    return blob_client.url  # Return the blob URL

# Helper function to process extracted text with Azure OpenAI
def process_with_openai(extracted_text):
    prompt = f"""You will receive a text... {extracted_text}"""
    response = client.completions.create(
        model=os.getenv("OPENAI_DEPLOYMENT_NAME"),
        prompt=prompt,
        max_tokens=1500
    )
    return response['choices'][0]['text']  # Assuming JSON format in response

# Helper function to store data in the Azure SQL Database
def store_in_database(extracted_data, filename, blob_url, extracted_text, file_extension):
    # Step 1: Insert document metadata
    new_document = Document(
        document_name=filename,
        url=blob_url,
        document_description=extracted_data.get('document_description', ''),
        extension=file_extension,
        text=extracted_text
    )
    db.session.add(new_document)
    db.session.commit()  # Commit to get document_id

    # Step 2: Insert accommodations and related data
    for accommodation in extracted_data['accommodations']:
        new_accommodation = Accommodation(
            accommodation_name=accommodation['accommodation_name'],
            accommodation_description=accommodation['accommodation_description'],
            verified=accommodation.get('verified', False),
            date_created=datetime.strptime(accommodation.get('date_updated', datetime.now().strftime("%Y-%m-%d")), "%Y-%m-%d"),
            document_id=new_document.document_id
        )

        # Add industries, injury locations, and injury natures
        for industry_name in accommodation['industries']:
            industry = db.session.query(Industry).filter_by(industry_name=industry_name).first()
            if industry:
                new_accommodation.industries.append(industry)

        for location_name in accommodation['injury_locations']:
            location = db.session.query(InjuryLocation).filter_by(injury_location_name=location_name).first()
            if location:
                new_accommodation.injury_locations.append(location)

        for nature_name in accommodation['injury_natures']:
            nature = db.session.query(InjuryNature).filter_by(injury_nature_name=nature_name).first()
            if nature:
                new_accommodation.injury_natures.append(nature)

        db.session.add(new_accommodation)
    
    db.session.commit()  # Commit all changes to the database

@accommodation_routes.route('/upload', methods=['POST'])
def upload_document():
    if 'file' not in request.files:
        return jsonify({"message": "No file part in the request"}), 400

    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"message": "No selected file"}), 400
    
    if file and allowed_file(file.filename):
        try:
            # Save the uploaded file
            filename = secure_filename(file.filename)
            file_extension = filename.rsplit('.', 1)[1].lower()
            file_path = os.path.join('/tmp', filename)
            file.save(file_path)

            # Step 1: Extract text from the document
            extracted_text = extract_text(file_path, file_extension)

            # Step 2: Process extracted text with Azure OpenAI
            extracted_data = process_with_openai(extracted_text)

            # Step 3: Upload the document to Azure Blob Storage
            blob_url = upload_to_blob(file_path, filename, file_extension)

            # Step 4: Store document and accommodation data in the database
            store_in_database(extracted_data, filename, blob_url, extracted_text, file_extension)

            # Step 5: Return success response
            return jsonify({
                "message": "Document uploaded successfully",
                "accommodations": extracted_data['accommodations']
            }), 200

        except Exception as e:
            db.session.rollback()  # Rollback database changes in case of error
            return jsonify({"message": "An error occurred during the process", "error": str(e)}), 500
    else:
        return jsonify({"message": "Unsupported file type"}), 400