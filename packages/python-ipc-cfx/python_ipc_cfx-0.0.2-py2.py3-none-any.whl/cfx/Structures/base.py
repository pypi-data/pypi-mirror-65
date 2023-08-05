"""Base classes and helper functions for CFX Structures and Enumerations."""
from enum import IntEnum
from numbers import Number
from json import dumps
from datetime import datetime
from dateutil.parser import parse
from ..utils.common import to_pascal_case


class CFXEnum(IntEnum):
    """Base enumeration class.

    Provides both __repr__ and __str__ methods to ease development, as well as a from_str constructor.
    """
    def __str__(self):
        return self._name_  # pylint: disable=no-member;

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.value == other.value  # pylint: disable=comparison-with-callable
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return "{}: {}".format(self.__class__.__name__, self._name_)  # pylint: disable=no-member;

    @classmethod
    def default(cls):
        """Returns the default (0) value for this Enumeration.

        Returns:
            CFXEnum: The default value for this CFXEnum.
        """
        return next(iter(cls))

    @classmethod
    def from_str(cls, in_value):
        """Class constructor from enumeration value.

        Args:
            in_value (str): Name of the desired enumeration value.

        Returns:
            CFXEnum: The object corresponding to the provided value.

        Raises:
            ValueError: If the provided value does not match any value in the CFXEnum.
        """
        for idx, value in enumerate([str(item) for item in list(cls)]):
            if value == in_value:
                return cls(idx)
        raise ValueError("{class_name}: Could not build object from value {value}".format(
            class_name=cls.__class__.__name__,
            value=in_value
        ))


class CFXStructure():
    """Base Structure class for CFX Structures.
    """
    def __str__(self):
        return dumps(self.as_dict(stringify=True))

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def as_dict(self, stringify=False, pascal_case=False):
        """Returns a dict representation of the object.

        Args:
            stringify (str): Optional - whether or not to turn supported objects into strings.
            pascal_case (bool): Optional - turns all keys into their PascalCase equivalent.

        Returns:
            dict: The object as a dictionary.
        """
        obj = {}
        for k in self.__dict__:
            key = to_pascal_case(k) if pascal_case else k
            val = self.__dict__[k]
            if isinstance(val, CFXEnum):
                obj[key] = str(val) if stringify else val
            elif isinstance(val, CFXStructure):
                obj[key] = val.as_dict(stringify=stringify, pascal_case=pascal_case)
            elif isinstance(val, list):
                obj[key] = _unroll_list(val, stringify=stringify, pascal_case=pascal_case)
            elif isinstance(val, datetime) and stringify:
                obj[key] = val.isoformat()
            else:
                obj[key] = val
        return obj

def _unroll_list(_list, stringify=False, pascal_case=False):
    if not isinstance(_list, list):
        raise TypeError("unroll_list: unroll_list only takes lists as arguments")
    out = []
    for value in _list:
        if isinstance(value, CFXEnum):
            if stringify:
                out.append(str(value) if not pascal_case else pascal_case(str(value)))
            else:
                out.append(str(value) if stringify else value)
        elif isinstance(value, CFXStructure):
            out.append(value.as_dict(stringify=stringify, pascal_case=pascal_case))
        elif isinstance(value, list):
            out.append(_unroll_list(value, stringify=stringify, pascal_case=pascal_case))
        else:
            out.append(value)
    return out


def load_basic(kwargs, name, type, default=None):
    """Helper function to load a basic type.

    Also supports PascalCase keys as a fallback.

    Args:
        kwargs (dict): A configuration object where the function will look up the provided name.
        name (str): Name of the configuration key to look up
        type (type): Expected type of the configuration value
        default (instance of type or None): Default value if there is no corresponding key in kwargs.

    Returns:
        instance of type or None: The value, or the default.

    Raises:
        TypeError:
            - If the provided default is not the right type
            - If the corresponding key in config is not of the right type
    """
    if type == "number":
        type = Number
    if default is not None and not isinstance(default, type):
        raise TypeError("load_basic: default value {default} is not of type {type}".format(
            default=default,
            type=type
        ))
    value = kwargs.get(name, default)
    if value is default:
        value = kwargs.get(to_pascal_case(name), default)
    if value is not None and not isinstance(value, type):
        try:
            if issubclass(type, Number) and isinstance(value, str):
                return type(value)
            if type == datetime:
                return parse(value)
        except Exception:
            raise TypeError("load_basic: {name} provided ({value}), but not of type {type}".format(
                name=name,
                type=type,
                value=value
            ))
    return value


def load_enum(kwargs, name, expected_type: CFXEnum, default=None):
    """Helper function to load an instance of CFXEnum

    Also supports PascalCase keys as a fallback.

    Args:
        kwargs (dict): A configuration object where the function will look up the provided name.
        name (str): Name of the configuration key to look up
        expected_type (type - subclass of CFXEnum): Expected CFXEnum type
        default (instance of type or None): Default value if there is no corresponding key in kwargs.

    Returns:
        CFXEnum or None: The value or the default.

    Raises:
        TypeError:
            - If the provided type is not a CFXEnum
            - If the provided default is not the right type
            - If the corresponding key in config is not of the right type
    """
    if not issubclass(expected_type, CFXEnum):
        raise TypeError("load_enum: load_enum only works with subclasses of CFXEnum, not %s" % expected_type.__name__)
    if default is not None and not isinstance(default, expected_type):
        raise TypeError("load_enum: default %s is not of type %s" % (default, expected_type.__name__))
    val = kwargs.get(name, default)
    if val is default:
        val = kwargs.get(to_pascal_case(name), default)
    if val is None:
        return None
    if isinstance(val, str):
        val = expected_type.from_str(val)
    if not isinstance(val, expected_type):
        raise TypeError("load_enum: {name} provided ({value}), but not a {expected_type}".format(
            name=name,
            value=val,
            expected_type=expected_type.__name__
        ))
    return val


def load_structure(kwargs, name, expected_structure, default=None):
    """Helper function to load an instance of CFXStructure

    Also supports PascalCase keys as a fallback.

    Args:
        kwargs (dict): A configuration object where the function will look up the provided name.
        name (str): Name of the configuration key to look up
        expected_structure (type - subclass of CFXStructure): Expected CFXStructure type
        default (instance of type or None): Default value if there is no corresponding key in kwargs.

    Returns:
        CFXStructure or None: The value or the default.

    Raises:
        TypeError:
            - If the provided type is not a CFXStructure
            - If the provided default is not the right type
            - If the corresponding key in config is not of the right type
    """
    if not issubclass(expected_structure, CFXStructure):
        raise TypeError(
            "load_structure: load_structure only works with subclasses of CFXStructure, not %s"
            % expected_structure.__name__
        )
    if default is not None and not isinstance(default, expected_structure):
        raise TypeError("load_structure: default %s is not of type %s" % (default, expected_structure.__name__))
    val = kwargs.get(name, default)
    if val is default:
        val = kwargs.get(to_pascal_case(name), default)
    if val is None:
        return None
    if isinstance(val, dict):
        val = expected_structure(**val)
    if not isinstance(val, expected_structure):
        raise TypeError("load_structure: {name} provided ({value}), but not a {expected_type}".format(
            name=name,
            value=val,
            expected_type=expected_structure.__name__
        ))
    return val


def load_list_enum(kwargs, name, expected_type, default=None):
    """Helper function to load a list of CFXEnums.

    Also supports PascalCase keys as a fallback.

    If a single dict is provided, it will be interpreted as a list containing one object.

    Args:
        kwargs (dict): A configuration object where the function will look up the provided name.
        name (str): Name of the configuration key to look up
        expected_type (type - subclass of CFXEnum): Expected CFXEnum type
        default (instance of type or None): Default value if there is no corresponding key in kwargs.

    Returns:
        list<CFXEnum> or None: The list or default

    Raises:
        TypeError:
            - If the provided type is not a CFXEnum
            - If the provided default is not the right type
            - If any instance of the corresponding key in config is not of the right type
    """
    default = default or []
    if not issubclass(expected_type, CFXEnum):
        raise TypeError(
            "load_list_enum: load_enum only works with subclasses of CFXEnum, not {}".format(
                expected_type.__name__
            )
        )
    if isinstance(default, expected_type):
        default = [default]
    if not isinstance(default, list):
        raise TypeError("load_list_enum: default {} is a wrong type".format(default))
    for item in default:
        if not isinstance(item, (str, expected_type)):
            raise TypeError("load_list_enum: default {} is a wrong type".format(item))
    values = kwargs.get(name, default)
    if values is default:
        values = kwargs.get(to_pascal_case(name), default)
    if values is None:
        return None
    if isinstance(values, str):
        values = [values]
    if not isinstance(values, list):
        raise TypeError("load_list_enum: {name} provided ({value}), but not a list".format(
            name=name,
            value=values
        ))
    out = []
    for val in values:
        if isinstance(val, str):
            val = expected_type.from_str(val)
        if not isinstance(val, expected_type):
            raise TypeError("load_enum: {name} provided ({value}), but not a {expected_type}".format(
                name=name,
                value=val,
                expected_type=expected_type.__name__
            ))
        out.append(val)
    return out


def load_list_structure(kwargs, name, expected_structure, default=None):
    """Helper function to load a list of CFXStructures.

    Also supports PascalCase keys as a fallback.

    If a single dict is provided, it will be interpreted as a list containing one object.

    Args:
        kwargs (dict): A configuration object where the function will look up the provided name.
        name (str): Name of the configuration key to look up
        expected_structure (type - subclass of CFXStructure): Expected CFXStructure type
        default (instance of type or None): Default value if there is no corresponding key in kwargs.

    Returns:
        list<CFXStructure> or None: The list or default

    Raises:
        TypeError:
            - If the provided type is not a CFXStructure
            - If the provided default is not the right type
            - If any instance of the corresponding key in config is not of the right type
    """
    default = default or []
    if not issubclass(expected_structure, CFXStructure):
        raise TypeError(
            "load_list_structure: load_list_structure only works with subclasses of CFXStructure, not {}".format(
                expected_structure.__name__
            )
        )
    if isinstance(default, (dict, expected_structure)):
        default = [default]
    if not isinstance(default, list):
        raise TypeError("load_list_structure: default {} is a wrong type".format(default))
    for item in default:
        if not isinstance(item, (dict, expected_structure)):
            raise TypeError("load_list_structure: default {} is a wrong type".format(item))
    values = kwargs.get(name, default)
    if values is default:
        values = kwargs.get(to_pascal_case(name), default)
    if values is None:
        return None
    if isinstance(values, dict):
        values = [values]
    if not isinstance(values, list):
        raise TypeError("load_list_structure: {name} provided ({value}), but not a list".format(
            name=name,
            value=values
        ))
    out = []
    for val in values:
        if isinstance(val, dict):
            val = expected_structure(**val)
        if not isinstance(val, expected_structure):
            raise TypeError("load_list_structure: {name} provided ({value}), but not a {expected_type}".format(
                name=name,
                value=val,
                expected_type=expected_structure.__name__
            ))
        out.append(val)
    return out
