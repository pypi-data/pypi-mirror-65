from typing import Union, Tuple, Dict, Sequence

import dataclasses

from .classify import classify, get_item_type


def serialize(T: type):
    """Creates a serializer for the type :T:. It handles dataclasses,
    sequences, typing.Optional and primitive types.

    :returns: A deserializer, converting a dict, list or primitive to :T:
    """

    return _serializers.get(classify(T), lambda x: lambda y: y)(T)


_serializers = {}


def _serializer(T: type):
    def decorator(f):
        _serializers[T] = f
        return f
    return decorator


@_serializer(Sequence)
@_serializer(Tuple)
def serialize_seq(T: type):
    item_type = get_item_type(T)

    def _serialize(data):
        return [serialize(item_type)(item) for item in data]
    return _serialize


@_serializer(dataclasses.dataclass)
def serialize_dataclass(T):
    fields = dataclasses.fields(T)

    def _serialize(data):
        if not isinstance(data, T):
            raise ValueError(
                f"{T.__name__}: Trying to serialize instance "
                f"of {type(data).__name__}")
        return {f.name: serialize(
            get_serialize_method(f))(getattr(data, f.name)) for f in fields}
    return _serialize


def get_serialize_method(f: dataclasses.Field) -> type:
    return f.metadata.get("serialize", f.type)


@_serializer(Union)
def serialize_union(T: type):
    types = T.__args__

    def _serialize(data):
        if not isinstance(data, types):
            raise ValueError(
                f"Union[{','.join(t.__name__ for t in types)}]:"
                f" Trying to serialize instance of {type(data).__name__}")
        return {"type": type(data).__name__,
                "arguments": serialize(type(data))(data)}
    return _serialize


@_serializer(Dict)
def serialize_dict(T: type):
    key_type, val_type = T.__args__

    def _serialize(data):
        return {
            serialize(key_type)(key): serialize(val_type)(val)
            for key, val in data.items()}
    return _serialize
