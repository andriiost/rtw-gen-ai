from flask import Blueprint
from ..controllers.accommodation_controller import (
    get_accommodation, 
    get_accommodations, 
    update_accommodation, 
    delete_accommodation,
    create_accommodation
)

accommodation_routes = Blueprint('accommodation_routes', __name__)

# Define routes and map them to controller functions
accommodation_routes.route('/accommodations/<int:id>', methods=['GET'])(get_accommodation)
accommodation_routes.route('/accommodations', methods=['GET'])(get_accommodations)
accommodation_routes.route('/accommodations/<int:accommodation_id>', methods=['PUT'])(update_accommodation)
accommodation_routes.route('/accommodations/<int:accommodation_id>', methods=['DELETE'])(delete_accommodation)
accommodation_routes.route('/accommodation', methods=['POST'])(create_accommodation)
