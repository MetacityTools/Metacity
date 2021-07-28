
def ensure_iterable(data):
    try:
        _ = iter(data)
        return data
    except TypeError:
        return [ data ]