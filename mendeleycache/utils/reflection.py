__author__ = 'kohn'


def get_class_attributes(target) -> [str]:
    return [attr for attr in dir(target) if not callable(attr) and not attr.startswith("__")]


def get_default(dct, key, default):
    if key in dct and not dct[key] is None:
        return dct[key]
    else:
        return default


def get_dict_if_key_exists(dct, key):
    if key in dct and not dct[key] is None:
        return dct[key]
    else:
        return dict()


def get_array_if_key_exists(dct, key):
    if key in dct and not dct[key] is None:
        return dct[key]
    else:
        return []
