def str_to_bool(value):
    """
    Converts string truthy/falsey strings to a bool
    Empty strings are false
    """
    if isinstance(value, str):
        value = value.strip().lower()
        if value in ['true', 't', 'yes', 'y']:
            return True
        elif value in ['false', 'f', 'no', 'n', '']:
            return False
        else:
            raise NotImplementedError("Unknown bool %s" % value)

    return value
