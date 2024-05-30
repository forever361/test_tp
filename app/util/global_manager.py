
def _init():
    """

    :return:
    """
    global _global_dict
    _global_dict = {}


def set_value(key, value):
    """

    :param key:
    :param value:
    :return:
    """
    _global_dict[key] = value


def get_value(key, def_value=None):
    """

    :param key:
    :param def_value:
    :return:
    """
    try:
        return _global_dict[key]
    except KeyError:
        return def_value
