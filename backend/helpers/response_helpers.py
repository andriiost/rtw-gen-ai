from flask import jsonify

def handle_error(message, status_code=400):
    """
    Return a standardized error response.

    This helper function generates a JSON response for error handling, 
    ensuring a consistent format for all API error responses.

    :param message: The error message to display.
    :param status_code: The HTTP status code for the error response (default is 400).
    :return: A Flask `jsonify` response object with the error message and status code.
    """
    return jsonify({"success": False, "message": message, "data": None}), status_code

def handle_success(message, data=None, status_code=200):
    """
    Return a standardized success response.

    This helper function generates a JSON response for successful API calls,
    ensuring a consistent format for all success responses.

    :param message: A success message to display.
    :param data: Optional data to include in the response (default is None).
    :param status_code: The HTTP status code for the success response (default is 200).
    :return: A Flask `jsonify` response object with the success message, optional data, and status code.
    """
    return jsonify({"success": True, "message": message, "data": data}), status_code
