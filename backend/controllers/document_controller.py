from flask import request
from sqlalchemy.orm import selectinload
from ..extensions import db
from ..models import Document, Accommodation
from ..schemas import DocumentSchema
from ..helpers.response_helpers import handle_error, handle_success
from ..helpers.file_helpers import allowed_file, extract_text, upload_to_blob_storage, store_document_in_db
from ..helpers.openai_helpers import process_with_openai
from ..blob_storage import blob_service_client, container_name
import os

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

        # Assuming file is from request.files['file']
        file = request.files['file']
        filename = file.filename

        # Get the file name and extension separately
        filename, file_extension = os.path.splitext(filename)

        # Remove the dot from the extension
        file_extension = file_extension[1:].lower()

        # Validate allowed file types
        if file and allowed_file(file.filename):
            existing_document = db.session.query(Document).filter_by(document_name=filename).first()
            if existing_document:
                return handle_error("Document with this name already exists", 400)

            # Extract text from the document
            extracted_text = extract_text(file, file_extension)
            # Process the extracted text (assumed dummy extracted data here)
            extracted_data = process_with_openai(filename, file_extension, extracted_text)

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
    
from azure.core.exceptions import ResourceNotFoundError

def delete_document(document_id):
    """
    Delete a document and its associated accommodations by document ID.

    This function deletes a document and all related accommodations from the database based on the provided document ID.
    If the document's blob is not found in Azure Blob Storage, it proceeds to delete the document from the database.

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
        try:
            blob_client.delete_blob()
        except ResourceNotFoundError:
            # If blob not found, log a message but continue with document deletion
            print(f"Blob {document.document_name} not found in Azure Blob Storage, proceeding with database deletion.")

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
