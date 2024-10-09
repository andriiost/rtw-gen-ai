import fitz
import docx2txt
from azure.storage.blob import ContentSettings
from ..extensions import db
from ..models import Document, Accommodation, InjuryNature, Industry, InjuryLocation
from datetime import datetime
from ..blob_storage import blob_service_client, container_name

# Allowed file extensions
ALLOWED_EXTENSIONS = {'pdf', 'docx'}

def allowed_file(filename):
    """
    Check if a file has an allowed extension.

    This function checks if the provided filename has an extension that is 
    within the allowed file types (PDF or DOCX).

    :param filename: The name of the file.
    :return: True if the file extension is allowed, False otherwise.
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text(file, extension):
    """
    Extract text from a file based on its extension.

    This function determines the file type (PDF or DOCX) and calls the appropriate
    function to extract the text from the file.

    :param file: The file object to extract text from.
    :param extension: The file extension (pdf or docx).
    :return: Extracted text from the file.
    :raises: ValueError if the file type is unsupported.
    """
    if extension == 'pdf':
        return extract_text_from_pdf(file)
    elif extension == 'docx':
        return extract_text_from_docx(file)
    else:
        raise ValueError("Unsupported file type")

def extract_text_from_pdf(file):
    """
    Extract text from a PDF file using PyMuPDF (Fitz).

    This function reads the PDF file and extracts its text content.

    :param file: The file object representing the PDF file.
    :return: A string containing the text extracted from the PDF.
    """
    try:
        file.seek(0)  # Reset file pointer to the beginning
        pdf_content = file.read()
        doc = fitz.open(stream=pdf_content, filetype="pdf")
        text = "\n".join([page.get_text() for page in doc])
        return text
    except Exception as e:
        print(f"Error extracting text from PDF: {str(e)}")
        raise e

def extract_text_from_docx(file):
    """
    Extract text from a DOCX file using docx2txt.

    This function reads the DOCX file and extracts its text content.

    :param file: The file object representing the DOCX file.
    :return: A string containing the text extracted from the DOCX file.
    """
    try:
        file.seek(0)  # Reset file pointer to the beginning
        text = docx2txt.process(file)
        return text
    except Exception as e:
        print(f"Error extracting text from DOCX: {str(e)}")
        raise e

def upload_to_blob_storage(filename, file_extension, file):
    """
    Upload a file to Azure Blob Storage.

    This function uploads the provided file to Azure Blob Storage and sets appropriate
    content type based on the file extension. It returns the URL of the uploaded file.

    :param filename: The name of the file to be uploaded.
    :param file_extension: The file extension (pdf or docx).
    :param file: The file object to upload.
    :return: The URL of the uploaded file in Azure Blob Storage.
    :raises: Exception if an error occurs during the upload process.
    """
    try:
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=filename)

        content_type = "application/pdf" if file_extension == "pdf" else "application/vnd.openxmlformats-officedocument.wordprocessingml.document"

        content_settings = ContentSettings(
            content_type=content_type,
            content_disposition='inline'  # Ensures the document opens in the browser
        )

        file.seek(0)  # Reset the file stream to the beginning
        blob_client.upload_blob(file, overwrite=True, content_settings=content_settings)

        return blob_client.url
    except Exception as e:
        print(f"Error uploading to Blob Storage: {str(e)}")
        raise e

def store_document_in_db(extracted_data, filename, file_extension, blob_url):
    """
    Store the document and its related accommodations in the database.

    This function stores the document metadata and its related accommodations 
    extracted from the document in the database.

    :param extracted_data: A dictionary containing document and accommodation details.
    :param filename: The name of the uploaded file.
    :param file_extension: The file extension (pdf or docx).
    :param blob_url: The URL of the uploaded file in Azure Blob Storage.
    :return: The newly created Document object.
    :raises: Exception if an error occurs while saving data to the database.
    """
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
