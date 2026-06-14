def success_response(data=None, message="OK", status_code=200):
    payload = {"status": "success", "message": message, "data": data}
    return payload, status_code


def error_response(message="Error", status_code=400, errors=None):
    payload = {"status": "error", "message": message, "errors": errors}
    return payload, status_code
