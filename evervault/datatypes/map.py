def map_header_type(data):
    if isinstance(data, int) or isinstance(data, float):
        return "number"
    elif isinstance(data, list):
        return "Array"
    elif isinstance(data, dict):
        return "object"
    elif isinstance(data, str):
        return "string"
    elif isinstance(data, bool):
        return "boolean"

def ensure_is_integer(data):
    try:
        float(data)
    except TypeError:
        return False
    else:
        return float(data).is_integer()