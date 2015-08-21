__author__ = 'kohn'


def get_class_attributes(target) -> [str]:
    return [attr for attr in dir(target) if not callable(attr) and not attr.startswith("__")]


def get_string_value_if_key_exists(dct, key) -> str:
    if key in dct and not dct[key] is None:
        return dct[key]
    else:
        return ""


def get_dict_if_key_exists(dct, key):
    if key in dct and not dct[key] is None:
        return dct[key]
    else:
        return dict()
