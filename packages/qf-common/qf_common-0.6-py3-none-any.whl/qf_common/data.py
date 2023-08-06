from enum import IntEnum


__BOOL_MAPPER = {
    True:  ['true', 't', 'yes', 'y', 'on', 'enable', 'enabled', '1'],
    False: ['false', 'f', 'no', 'n', 'off', 'disable', 'disabled', '0'],
}


def any_to_bool(value: (bool, int, float, str), default: bool = None) -> bool:
    if isinstance(value, (bool, int, float)):
        return bool(value)

    for key, aliases in __BOOL_MAPPER.items():
        if str(value).lower() in aliases:
            return key

    else:
        if default is None:
            from argparse import ArgumentTypeError
            raise ArgumentTypeError('Can\'t convert \'%s\' to boolean value' % value)

    return default


def any_to_int(value: any) -> int:
    if isinstance(value, IntEnum):
        value = value.value

    elif value is None:
        value = 0

    assert isinstance(value, int), \
        'Wrong index type provided'

    return value


def iterable(obj: any, save_none_value: bool = False) -> tuple:
    if obj is None and not save_none_value:
        return tuple()  # making empty tuple (None means empty tuple required)

    # from requests.structures import CaseInsensitiveDict
    if isinstance(obj, (str, dict,)):  # CaseInsensitiveDict)):
        return obj,     # making tuple from string or dict (string is iterable by characters)

    if hasattr(obj, '__iter__'):
        return obj      # returning iterable object as is without any conversion

    return obj,         # converting the object to the tuple by default


def pick_index_safe(elements, index: int = None):
    index = any_to_int(index)

    # normalizing the index (None means 0, -1 means last, etc)
    index += len(elements)
    from sys import maxsize as max_int
    index %= len(elements) or max_int

    return elements[index] \
        if index in range(len(elements)) \
        else None


def pick_attributes_safe(element, *attrs):
    attr_value = element

    for attr in attrs:
        attr_value = getattr(
            attr_value, attr, None)

    return attr_value
