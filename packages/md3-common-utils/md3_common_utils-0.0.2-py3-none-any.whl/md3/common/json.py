def get_dict_from_json_recursive(json, fields, base_key=None, composed_key=None, separator="."):
    """
    Helper function to convert json into keys
    Example:
        for this input -> a = {"b": "zzzz", "c": "hhhh"}
        fields dict will be filled with
        fields = {"a.b": "zzzz", "a.c": "hhhh"}
    Note: due to it's recursivity this will work for all dict levels
    """

    if base_key and composed_key is None:
        composed_key = base_key

    if isinstance(json, dict):
        for k, v in json.items():
            if isinstance(v, dict):
                composed_key = "%s%s%s" % (composed_key, separator, k) if composed_key else k
                get_dict_from_json_recursive(json=v, fields=fields, base_key=composed_key)
            else:
                composed_key = "%s%s%s" % (composed_key, separator, k) if composed_key else k
                fields[composed_key] = v

            composed_key = base_key if base_key else None
    else:
        fields[composed_key] = json


def update_recursive(d, u):
    """
    Helper function update some fields recursively in a dictionary, this allows to update
    some dict inside a dict without overwriting the unchanged fields
    d is the dictionary we want to update
    u is the dictionary with the fields we want to update in d
    Note: only the fields existing in u will be updated in the destination -> d
    """

    for k, v in u.items():
        if isinstance(v, dict):
            d[k] = update_recursive(d.get(k, {}), v)
        else:
            d[k] = v

    return d
