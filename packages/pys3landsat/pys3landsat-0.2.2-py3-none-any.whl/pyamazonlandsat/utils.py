def to_list_name(name):
    """Return a splited name by `_`.

    :param name: name of the product.
    :type name: str.
    """
    return name.split('_')

def get_path_row_from_name(name):
    """Get the path row data from product name.

    :param name: name of the product.
    :type name: str.
    """
    lname = to_list_name(name)
    path = lname[2][:3]
    row = lname[2][3:]
    return (path, row)

def get_acquisition_time(name):
    """Get acquisition time from the product name.

    :param name: name of the product.
    :type name: str.
    """
    return to_list_name(name)[3]

def get_processing_date(name):
    """Get the processing date from the product name.

    :param name: name of the product.
    :type name: str.
    """
    return to_list_name(name)[4]

def get_collection_number(name):
    """Get the collection number from the product name.

    :param name: name of the product.
    :type name: str.
    """
    return to_list_name(name)[5]

def get_collection_category(name):
    """Get the collection category from the product name.

    :param name: name of the product.
    :type name: str.
    """
    return to_list_name(name)[6]

def get_satellite(name):
    """Get the satelllite codename  from the product name.

    :param name: name of the product.
    :type name: str.
    """
    return to_list_name(name)[0]


