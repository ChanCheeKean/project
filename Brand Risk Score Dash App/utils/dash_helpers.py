# Functions which make life easier

def parse_options(options):
    """
    Helper Function to bring options to right format.

    :param options: List or dictionary
        - A list of option strings, which will be identical for label
          and value.
        - A dictionary of format {'label1': 'val1', 'label2': 'val2'}

    :return: A list of dictionaries as needed by many dcc components.
        See eg documentation of dcc.Dropdown.
    """
    opt_list = []
    if isinstance(options, dict):
        # Dictionary
        for label in options:
            opt_list.append({'label': label,
                             'value': options[label]})
    else:
        for item in options:
            opt_list.append({'label': item,
                             'value': item})

    return opt_list


