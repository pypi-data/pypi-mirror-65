def get_bool(value):
    """
    Convert value to a boolean
    """
    if isinstance(value, bool):
        return value
    return str(value).lower() in ['yes', 'y', '1', 'on', 'true', 't']
