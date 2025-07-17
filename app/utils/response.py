def success_response(data=None, message="Success", status_code=200):
    return {
        "status": "success",
        "message": message,
        "data": data
    }, status_code


def error_response(message="Something went wrong", status_code=400):
    return {
        "status": "error",
        "message": message,
        "data": None
    }, status_code

def get_schema_dict(schema_cls):
    return {
        'type': 'object',
        'properties': {
            field_name: {
                'type': 'string',  # basic type; you can improve based on field type
                'example': 'demo'
            }
            for field_name in schema_cls().fields
        },
        'required': list(schema_cls().fields.keys())
    }
