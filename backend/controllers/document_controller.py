from flask import request
from sqlalchemy.orm import selectinload
from ..extensions import db
from ..models import Document, Accommodation
from ..schemas import DocumentSchema
from ..helpers.response_helpers import handle_error, handle_success
from ..helpers.file_helpers import allowed_file, extract_text, upload_to_blob_storage, store_document_in_db
from ..helpers.openai_helpers import process_with_openai
from ..blob_storage import blob_service_client, container_name

def get_document_with_accommodations(document_id):
    """
    Retrieve a document and its associated accommodations by document ID.

    This function fetches a document and its related accommodations from the database based on the provided document ID.
    It uses SQLAlchemy's `selectinload` to eagerly load related accommodations, industries, injury locations, and injury natures
    to optimize performance.

    :param document_id: The ID of the document to retrieve.
    :return: A JSON response containing the document details and accommodations or an error message.
    """
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
    
def upload_document():
    """
    Upload a document and its accommodations.

    This function handles the upload of a document file, processes the file to extract its content, and stores
    the document and its associated accommodations in the database. The document file is uploaded to Azure Blob Storage.

    :return: A JSON response indicating success or an error message.
    """
    try:
        # Check if a file part exists in the request
        if 'file' not in request.files:
            return handle_error("No file part in the request", 400)

        file = request.files['file']
        filename = file.filename
        
        if filename == '':
            return handle_error("No selected file", 400)

        file_extension = filename.rsplit('.', 1)[1].lower()

        # Validate allowed file types
        if file and allowed_file(filename):
            existing_document = db.session.query(Document).filter_by(document_name=filename).first()
            if existing_document:
                return handle_error("Document with this name already exists", 400)

            # Extract text from the document
            extracted_text = extract_text(file, file_extension)
            extracted_data = process_with_openai(filename, file_extension, extracted_text)
            # Process the extracted text (assumed dummy extracted data here)
            # extracted_data = {'accommodations': [{'accommodation_name': 'Brick tongs', 'accommodation_description': 'Brick tongs allow lifting of a half dozen bricks at a time with a neutral wrist and power grip posture.', 'injury_location_name': 'Wrist(s)', 'industry_name': 'Construction', 'injury_nature_name': 'Sprains and strains', 'verified': False, 'date_created': '2024-10-07'}, {'accommodation_name': 'Lift on a wheeled platform', 'accommodation_description': 'This lift can be placed on a wheeled platform that will move along the wall being built. It eliminates the lift of each cinder block from the bricklayer.', 'injury_location_name': 'Multiple body parts', 'industry_name': 'Construction', 'injury_nature_name': 'Multiple traumatic injuries', 'verified': False, 'date_created': '2024-10-07'}, {'accommodation_name': 'Mortar silos', 'accommodation_description': 'The industry is recommending moving to mortar silos where pre-mixed mortar is delivered to a silo placed on-site and mortar is dispensed into a wheelbarrow with no lifting of bags of mix. These are useful in new housing developments where multiple houses are being built or commercial developments where large buildings are being constructed.', 'injury_location_name': 'Lower back (lumbar, sacral, coccygeal regions)', 'industry_name': 'Construction', 'injury_nature_name': 'Sprains and strains', 'verified': False, 'date_created': '2024-10-07'}, {'accommodation_name': 'Mortar stands', 'accommodation_description': 'Mortar stands are a great tool that raises the mortar to ensure repeated bending is not required. The base shown allows 2 different heights but there are stands of varying heights.', 'injury_location_name': 'Lower back (lumbar, sacral, coccygeal regions)', 'industry_name': 'Construction', 'injury_nature_name': 'Sprains and strains', 'verified': False, 'date_created': '2024-10-07'}, {'accommodation_name': 'Scaffold with hand lever', 'accommodation_description': 'This model has a hand lever that cranks the plank up one notch at a time or lowers one notch at a time. This results in the bricklayer working at the optimum postures at all times, as they can make incremental adjustments to the plank height with very little effort and time away from the work. These are purchased one frame at a time and a minimum of 2 are required but work platforms can be set-up the length of a house or one section at a time making this an affordable tool for independent operators.', 'injury_location_name': 'Multiple body parts', 'industry_name': 'Construction', 'injury_nature_name': 'Multiple traumatic injuries', 'verified': False, 'date_created': '2024-10-07'}], 'document_description': 'The document is a newsletter focused on accommodations in the construction industry, particularly for bricklayers and stonemasons. It discusses the physical demands of the work and presents several tools and methods to reduce these demands and the risk of injury. These include brick tongs, a lift on a wheeled platform, mortar silos, mortar stands, and a scaffold with a hand lever.', 'document_name': 'Accommodations - Construction - Bricklayer (WSIB Newsletter).pdf', 'extension': 'pdf'}

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
    
def delete_document(document_id):
    """
    Delete a document and its associated accommodations by document ID.

    This function deletes a document and all related accommodations from the database based on the provided document ID.

    :param document_id: The ID of the document to delete.
    :return: A JSON response indicating success or an error message.
    """
    try:
        # Step 1: Fetch the document by ID
        document = db.session.query(Document).filter_by(document_id=document_id).first()

        if not document:
            return handle_error("Document not found", 404)

        # Get the blob client using the document's URL
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=document.document_name)

        # Attempt to delete the blob
        blob_client.delete_blob()

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
        # Log error and return generic error response
        print(f"Error deleting document: {str(e)}")
        return handle_error("An internal server error occurred while deleting the document", 500)