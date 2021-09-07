def getattrdot(obj, path, default=None):
    if path is None:
        return obj

    for a in path.split('.'):
        if hasattr(obj, a):
            obj = getattr(obj, a)
        else:
            return default
    return obj
