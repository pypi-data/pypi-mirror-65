import sys
from typing import Union, Tuple, Any, Dict, Optional, Sequence
import collections

import dataclasses

# Starting with python 3.7, the typing module has a new API
__origin_attr__ = "__extra__" if sys.version_info < (3, 7) else "__origin__"

_classifiers = []


def _classifier(f):
    _classifiers.append(f)
    return f


def classify(T: type):
    for classifier in _classifiers:
        C = classifier(T)
        if C is not None:
            return C
    return None


@_classifier
def classify_any(T: type):
    if T is not Any:
        return None
    return Any


@_classifier
def classify_tuple(T: type):
    if getattr(T, "__origin__", None) is not Tuple:
        return None
    return Tuple


@_classifier
def classify_seq(T: type):
    seq_type = getattr(T, __origin_attr__, None)
    if (isinstance(seq_type, type) and
            issubclass(seq_type, collections.abc.Sequence)):
        return Sequence
    return None


@_classifier
def classify_dataclass(T: type):
    if dataclasses.is_dataclass(T):
        return dataclasses.dataclass
    return None


@_classifier
def classify_optional(T: type):
    if getattr(T, "__origin__", None) is not Union:
        return None
    if isinstance(None, T.__args__) and len(T.__args__) == 2:
        return Optional
    return None


@_classifier
def classify_union(T: type):
    if getattr(T, "__origin__", None) is Union:
        return Union
    return None


@_classifier
def classify_dict(T: type):
    t_origin = getattr(T, __origin_attr__, None)
    if t_origin is not dict:
        return None
    return Dict


def get_item_type(T: type) -> type:
    seq_type = getattr(T, __origin_attr__, None)
    try:
        return T.__args__[0]
    except AttributeError:
        raise ValueError(
            f"Sequence of type {seq_type.__name__} without item type")
