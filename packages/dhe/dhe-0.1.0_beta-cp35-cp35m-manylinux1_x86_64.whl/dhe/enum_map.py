from collections import OrderedDict


def EnumMap(base_type):
    class EnumMapType(base_type):
        items = OrderedDict()
        reverse_lookup = {}
        default = None

        @classmethod
        def add_item(cls, name, val):
            if name in cls.items:
                raise ValueError(
                    "An object with key {} is allready in EnumMap".format(name))
            cls.items[name] = val
            cls.reverse_lookup[val] = name
            if cls.default is None:
                cls.default = val

        @classmethod
        def item(cls, f):
            cls.add_item(f.__name__, f)
            return f

        @classmethod
        def item_with_key(cls, key):
            def decorator(f):
                cls.add_item(key, f)
                return f
            return decorator

    return EnumMapType
