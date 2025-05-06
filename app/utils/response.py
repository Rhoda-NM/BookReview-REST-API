from flask import jsonify

def success_response(data=None, message="Success", status_code=200):
    """
    Returns a success response in JSON format."""
    
    response = {"Sucess": True}
    if message:
        response["message"] = message
    if data:
        response["data"] = data
    return jsonify(response), status_code

def error_response(message, errors=None, status_code=400):
    """Standard error response."""
    response = {"Success": False, "message": message}
    if errors:
        response["errors"] = errors
    return jsonify(response), status_code
    