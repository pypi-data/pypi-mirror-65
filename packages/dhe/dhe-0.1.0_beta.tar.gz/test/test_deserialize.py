import unittest
import typing
from dataclasses import dataclass

from dhe import deserialize


class TestSerialize(unittest.TestCase):
    def test_deserialize(self):
        @dataclass
        class Y:
            x: int
            y: typing.List[bool]

        @dataclass
        class X:
            a: int
            pack: Y

        data = {"a": 1, "pack": {"x": 1, "y": [True, False]}}
        x = deserialize.deserialize(X)(data)

        self.assertEqual(x, X(a=1, pack=Y(x=1, y=[True, False])))

        # typing.Dict
        @dataclass
        class Z:
            a: int
            dct: typing.Dict[int, str]

        data = {"a": 1, "dct": {1: "x", 2: "y"}}
        z = deserialize.deserialize(Z)(data)

        self.assertEqual(z, Z(a=1, dct=data["dct"]))

        # typing.Optional
        self.assertEqual(deserialize.deserialize(
            typing.Optional[int])(None), None)
        self.assertEqual(deserialize.deserialize(
            typing.Optional[int])(1), 1)
        self.assertEqual(deserialize.deserialize(
            typing.Any)(1), 1)
        self.assertEqual(deserialize.deserialize(
            typing.Any)("1"), "1")

    def test_deserialize_tuple(self):
        self.assertEqual(deserialize.deserialize(
            typing.Tuple[int, float])([1., 3]), (1, 3.))

    def test_deserialize_union(self):
        @dataclass
        class X:
            x: int
        self.assertEqual(deserialize.deserialize(
            typing.Union[int, X, bool])({
                "type": "X", "arguments": {"x": 1}}),
            X(1))
        self.assertEqual(deserialize.deserialize(
            typing.Union[int, X, bool])({
                "type": "int", "arguments": 1}),
            1)
