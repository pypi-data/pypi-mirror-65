

# to find dict in a dict
def find_dict(key, dictionary):
    for k, v in dictionary.items():
        if k == key:
            yield v
        elif isinstance(v, dict):
            for result in find_dict(key, v):
                yield result
        elif isinstance(v, list):
            for d in v:
                if isinstance(d, dict):
                    for result in find_dict(key, d):
                        yield result

# to find dict in a dict key = value
def find_dict2(key, val, dictionary):
    for k, v in dictionary.items():
        if k == key and v == val:
            yield dictionary
        elif isinstance(v, dict):
            for result in find_dict2(key, val, v):
                yield result
        elif isinstance(v, list):
            for d in v:
                if isinstance(d, dict):
                    for result in find_dict2(key, val, d):
                        yield result

