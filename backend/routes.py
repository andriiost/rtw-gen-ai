from flask import Blueprint, jsonify, request
from werkzeug.utils import secure_filename
from .models import Accommodation, Industry, InjuryLocation, InjuryNature, Document
from .schemas import AccommodationSchema, DocumentSchema
from sqlalchemy.orm import selectinload
from sqlalchemy import asc, desc
from . import db
from datetime import datetime
from azure.storage.blob import BlobServiceClient, ContentSettings
from openai import AzureOpenAI
import os
import fitz
import docx2txt
import json
import io

# Create a blueprint
accommodation_routes = Blueprint('accommodation_routes', __name__)

# Azure Blob Storage setup
blob_service_client = BlobServiceClient(account_url=f"https://{os.getenv('AZURE_STORAGE_ACCOUNT')}.blob.core.windows.net", credential=os.getenv('AZURE_BLOB_KEY'))
container_name = os.getenv("AZURE_BLOB_CONTAINER")

deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")

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
def extract_text(file, extension):
    if extension == 'pdf':
        return extract_text_from_pdf(file)
    elif extension == 'docx':
        return extract_text_from_docx(file)
    else:
        raise ValueError("Unsupported file type")
    
# Extract text from PDF files (using PyMuPDF - fitz)
def extract_text_from_pdf(file):
    # Reset the file pointer to the beginning (in case it was read already)
    file.seek(0)
    
    # Read the entire file content into memory
    pdf_content = file.read()

    # Open the file content with PyMuPDF
    doc = fitz.open(stream=pdf_content, filetype="pdf")  # Pass file content as stream
    text = "\n".join([page.get_text() for page in doc])
    return text

# Extract text from DOCX files (using docx2txt or similar)
def extract_text_from_docx(file):
    # Reset the file pointer to the beginning (in case it was read already)
    file.seek(0)
    text = docx2txt.process(file)  # Pass file object directly to docx2txt
    return text

# Helper function to upload to Azure Blob Storage directly from memory
def upload_to_blob_storage(filename, file_extension, file):
    # Get a blob client
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=filename)

    # Set the correct Content-Type based on the file extension
    content_type = "application/pdf" if file_extension == "pdf" else "application/vnd.openxmlformats-officedocument.wordprocessingml.document"

    # ContentSettings to ensure the file opens in the browser
    content_settings = ContentSettings(
        content_type=content_type,
        content_disposition='inline'  # Ensures the document opens in the browser
    )

    # Upload the file directly to Blob Storage from memory
    try:
        file.seek(0)  # Reset the file stream to the beginning
        blob_client.upload_blob(file, overwrite=True, content_settings=content_settings)
        # Return the blob URL
        return blob_client.url
    except Exception as e:
        print(f"Error uploading to Blob Storage: {e}")
        raise e

# Helper function to process extracted text with Azure OpenAI
def process_with_openai(filename, file_extension, extracted_text):
    prompt = f"""
    You will receive a text containing information about multiple accommodations. Extract each accommodation from the text with the following details:
    - Accommodation Name: The specific tool or method being used to accommodate workers. Retrieve directly from the text; do not create or alter names;;
    - Description: A detailed explanation of the accommodation.Get this info from the text directly. Retrieve directly from the text; do not create or alter description;ter names;
    - Injury Location Name: Choosing only from the list: {"Body systems", "Multiple body parts", "Cranial region, including skull", "Leg(s)", "Lower back (lumbar, sacral, coccygeal regions)", "Shoulder", "Ankle(s)", "Finger(s), fingernail(s)", "Arm(s)", "Wrist(s)", "Not Coded", "Foot (feet), except toe(s)", "Chest, including ribs, internal organs", "Pelvic region", "Upper extremities, unspecified, NEC", "Multiple trunk locations", "Multiple lower extremities locations", "Hand(s), except finger(s)", "Upper back (cervical, thoracic regions)", "Multiple back regions", "Abdomen", "Back, unspecified, NEC", "Head, unspecified, NEC", "Eye(s)", "Face", "Toe(s), toenail(s)", "Ear(s)", "Multiple head locations", "Lower extremities, unspecified, NEC", "Trunk, unspecified, NEC", "Other body parts including unclassified, NEC"} identify the part of the body that the accommodation aims to protect or assist;
    - Industry Name: Choosing only from the list: {"Agriculture, forestry, fishing, and hunting", "Mining, quarrying, and oil and gas extraction", "Utilities", "Construction", "Manufacturing", "Wholesale trade", "Retail trade", "Transportation and warehousing", "Information and cultural industries", "Finance and insurance", "Real estate and rental and leasing", "Professional, scientific, and technical services", "Management of companies and enterprises", "Administrative and support, waste management, and remediation services", "Educational services", "Health care and social assistance", "Arts, entertainment, and recreation", "Accommodation and food services", "Other services (except public administration)", "Public administration"} identify the industry in which the accommodation is used (e.g., Construction). If there is no industry specified say "Multiple";
    - Injury Nature Name: Choosing only from the list: {"Sprains and strains", "Psychiatric", "Fractures", "Concussion", "Traumatic injuries, disorders, complications, unspecified, NEC", "Multiple traumatic injuries", "Bruises, contusions", "COVID-19 novel coronavirus", "Intracranial injuries excluding concussions"} identify the nature of the injury that the accommodation aims to address. If there is no nature specified say "Multiple".
    - Summary: please create a summary of the document so that any one who wishes to know what the document is about can get a brief overview. Please take ideas directly from the document only.

    Format the extracted data as a JSON object, with an array if multiple are mentioned in the text. Use the following structure:
    {{
      "accommodations": [
        {{
         "accommodation_name": "",
          "accommodation_description": "",
          "injury_location_name": "",
          "industry_name": "",
          "injury_nature_name": ""
        }}
      ], 
      "document_description": ""
    }}
    Title: {filename}
    Text: {extracted_text}
    """
    response = client.chat.completions.create(
        model=deployment,
        messages=[
            {"role": "system", "content": "You are a helpful assistant designed to extract data from text and format it as JSON object."},
            {"role": "user", "content": prompt}
        ],
        # past_messages=10,
        max_tokens=2000,
        temperature=0.7,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None,
        stream=False
    )
    # Parse the response JSON string into a Python dictionary
    extracted_json = json.loads(response.choices[0].message.content)
    # Add verified and date_created fields
    current_date = datetime.now().strftime("%Y-%m-%d")  # Current date only
    for accommodation in extracted_json['accommodations']:
        accommodation['verified'] = False
        accommodation['date_created'] = current_date  # Assuming JSON format in response
    
    extracted_json["document_name"] = filename
    extracted_json["extension"] = file_extension
    return extracted_json

# Helper function to store data in the database
def store_document_in_db(extracted_data, filename, file_extension, blob_url):
    try:
        # Insert document into the database
        new_document = Document(
            document_name=filename,
            url=blob_url,
            document_description=extracted_data['document_description'],
            extension=file_extension
        )
        db.session.add(new_document)
        db.session.commit()  # Commit to generate document_id

        # Insert accommodations and related data
        for accommodation_data in extracted_data['accommodations']:
            new_accommodation = Accommodation(
                accommodation_name=accommodation_data['accommodation_name'],
                accommodation_description=accommodation_data['accommodation_description'],
                verified=accommodation_data['verified'],
                date_created=datetime.strptime(accommodation_data['date_created'], "%Y-%m-%d"),
                document_id=new_document.document_id
            )
            db.session.add(new_accommodation)
            db.session.commit()  # Commit to get accommodation_id

            # Handle industries
            industry = db.session.query(Industry).filter_by(industry_name=accommodation_data["industry_name"]).first()
            if industry:
                new_accommodation.industries.append(industry)
            
            # Handle injury locations
            injury_location = db.session.query(InjuryLocation).filter_by(injury_location_name=accommodation_data["injury_location_name"]).first()
            if injury_location:
                new_accommodation.injury_locations.append(injury_location)

            # Handle injury natures
            injury_nature = db.session.query(InjuryNature).filter_by(injury_nature_name=accommodation_data["injury_nature_name"]).first()
            if injury_nature:
                new_accommodation.injury_natures.append(injury_nature)
            
            db.session.commit()

        return new_document
    except Exception as e:
        db.session.rollback()
        raise Exception(f"Error saving to database: {str(e)}")

# Upload document and its accommodations
@accommodation_routes.route('/documents', methods=['POST'])
def upload_document():
    try:
        # Check if a file part exists in the request
        if 'file' not in request.files:
            return handle_error("No file part in the request", 400)

        file = request.files['file']
        filename = secure_filename(file.filename)
        
        if filename == '':
            return handle_error("No selected file", 400)

        file_extension = filename.rsplit('.', 1)[1].lower()

        # Validate allowed file types
        if file and allowed_file(file.filename):
            existing_document = db.session.query(Document).filter_by(document_name=filename).first()
            if existing_document:
                return handle_error("Document with this name already exists", 400)

            # Extract text from the document
            extracted_text = extract_text(file, file_extension)
            # extracted_data = process_with_openai(filename, file_extension, extracted_text)
            # Process the extracted text (assumed dummy extracted data here)
            extracted_data = {'accommodations': [{'accommodation_name': 'Brick tongs', 'accommodation_description': 'Brick tongs allow lifting of a half dozen bricks at a time with a neutral wrist and power grip posture.', 'injury_location_name': 'Wrist(s)', 'industry_name': 'Construction', 'injury_nature_name': 'Sprains and strains', 'verified': False, 'date_created': '2024-10-07'}, {'accommodation_name': 'Lift on a wheeled platform', 'accommodation_description': 'This lift can be placed on a wheeled platform that will move along the wall being built. It eliminates the lift of each cinder block from the bricklayer.', 'injury_location_name': 'Multiple body parts', 'industry_name': 'Construction', 'injury_nature_name': 'Multiple traumatic injuries', 'verified': False, 'date_created': '2024-10-07'}, {'accommodation_name': 'Mortar silos', 'accommodation_description': 'The industry is recommending moving to mortar silos where pre-mixed mortar is delivered to a silo placed on-site and mortar is dispensed into a wheelbarrow with no lifting of bags of mix. These are useful in new housing developments where multiple houses are being built or commercial developments where large buildings are being constructed.', 'injury_location_name': 'Lower back (lumbar, sacral, coccygeal regions)', 'industry_name': 'Construction', 'injury_nature_name': 'Sprains and strains', 'verified': False, 'date_created': '2024-10-07'}, {'accommodation_name': 'Mortar stands', 'accommodation_description': 'Mortar stands are a great tool that raises the mortar to ensure repeated bending is not required. The base shown allows 2 different heights but there are stands of varying heights.', 'injury_location_name': 'Lower back (lumbar, sacral, coccygeal regions)', 'industry_name': 'Construction', 'injury_nature_name': 'Sprains and strains', 'verified': False, 'date_created': '2024-10-07'}, {'accommodation_name': 'Scaffold with hand lever', 'accommodation_description': 'This model has a hand lever that cranks the plank up one notch at a time or lowers one notch at a time. This results in the bricklayer working at the optimum postures at all times, as they can make incremental adjustments to the plank height with very little effort and time away from the work. These are purchased one frame at a time and a minimum of 2 are required but work platforms can be set-up the length of a house or one section at a time making this an affordable tool for independent operators.', 'injury_location_name': 'Multiple body parts', 'industry_name': 'Construction', 'injury_nature_name': 'Multiple traumatic injuries', 'verified': False, 'date_created': '2024-10-07'}], 'document_description': 'The document is a newsletter focused on accommodations in the construction industry, particularly for bricklayers and stonemasons. It discusses the physical demands of the work and presents several tools and methods to reduce these demands and the risk of injury. These include brick tongs, a lift on a wheeled platform, mortar silos, mortar stands, and a scaffold with a hand lever.', 'document_name': 'Accommodations - Construction - Bricklayer (WSIB Newsletter).pdf', 'extension': 'pdf'}

            # Upload to Azure Blob Storage
            blob_url = upload_to_blob_storage(filename, file_extension, file)

            # Store the document and accommodations in the database
            new_document = store_document_in_db(extracted_data, filename, file_extension, blob_url)

            # Serialize the newly stored document and accommodations
            document_schema = DocumentSchema()
            document_data = document_schema.dump(new_document)

            return handle_success("Document uploaded successfully", document_data)

        else:
            return handle_error("Unsupported file type", 400)

    except Exception as e:
        return handle_error(f"An error occurred: {str(e)}", 500)

# Fetch Document and its associated accommodations
@accommodation_routes.route('/documents/<int:document_id>', methods=['GET'])
def get_document_with_accommodations(document_id):
    try:
        document = db.session.query(Document)\
            .options(
                selectinload(Document.accommodations).selectinload(Accommodation.industries),
                selectinload(Document.accommodations).selectinload(Accommodation.injury_locations),
                selectinload(Document.accommodations).selectinload(Accommodation.injury_natures)
            ).filter_by(document_id=document_id).first()

        if not document:
            return handle_error("Document not found", 404)

        document_schema = DocumentSchema()
        document_data = document_schema.dump(document)

        return handle_success("Document and accommodations retrieved successfully", document_data)

    except Exception as e:
        return handle_error(f"An error occurred: {str(e)}", 500)

# Delete Document and its associated accommodations
@accommodation_routes.route('/documents/<int:document_id>', methods=['DELETE'])
def delete_document(document_id):
    try:
        # Step 1: Fetch the document by ID
        document = db.session.query(Document).filter_by(document_id=document_id).first()

        if not document:
            return handle_error("Document not found", 404)

        # Step 2: Remove document from Azure Blob Storage
        try:
            # Get the blob client using the document's URL
            blob_client = blob_service_client.get_blob_client(container=container_name, blob=document.document_name)

            # Attempt to delete the blob
            blob_client.delete_blob()
        except Exception as e:
            # Log the error, but proceed with the deletion from the database
            print(f"Error deleting from Azure Blob Storage: {e}")

        # Step 3: Delete associated accommodations (Cascade delete if foreign keys are set up)
        accommodations = db.session.query(Accommodation).filter_by(document_id=document_id).all()
        for accommodation in accommodations:
            db.session.delete(accommodation)

        # Step 4: Delete the document from the database
        db.session.delete(document)
        db.session.commit()

        # Step 5: Return success response
        return handle_success("Document and associated accommodations deleted successfully", {"document_id": document_id})

    except Exception as e:
        # Handle unexpected errors
        db.session.rollback()  # Rollback in case of errors
        return handle_error(f"An error occurred during the deletion process: {str(e)}", 500)

