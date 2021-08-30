
def ensure_iterable(data):
    try:
        _ = iter(data)
        return data
    except TypeError:
        return [ data ]


def ensure_list_like(data):
    if isinstance(data, list) or isinstance(data, tuple):
        return data
    return [ data ]
    