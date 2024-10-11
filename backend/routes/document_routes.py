from flask import Blueprint
from ..controllers.document_controller import (
    upload_document, 
    get_document_with_accommodations, 
    delete_document
)

document_routes = Blueprint('document_routes', __name__)

# Define routes and map them to controller functions
document_routes.route('/documents', methods=['POST'])(upload_document)
document_routes.route('/documents/<int:document_id>', methods=['GET'])(get_document_with_accommodations)
document_routes.route('/documents/<int:document_id>', methods=['DELETE'])(delete_document)
