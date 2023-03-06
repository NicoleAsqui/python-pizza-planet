from flask import jsonify
from functools import wraps


def base_service(base_controller):
    @wraps(base_controller)
    def wrapper(*args, **kwargs):
        items, error = base_controller(*args, **kwargs)
        response = items if not error else {"error": error}
        status_code = 200 if items else 404 if not error else 400
        return jsonify(response), status_code

    return wrapper