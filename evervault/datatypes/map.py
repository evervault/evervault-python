def map_header_type(data):

    if isinstance(data, bool):
        return "boolean"
    elif isinstance(data, int) or isinstance(data, float):
        return "number"
    elif isinstance(data, str):
        return "string"
