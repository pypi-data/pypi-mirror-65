#!/usr/bin/env python3

import unittest
from dhe import model
from dhe.serialize import serialize
from dhe.deserialize import deserialize


class TestDataInterface(unittest.TestCase):
    def test_serialize(self):
        cfg = model.DHEConfiguration()
        dct = serialize(model.DHEConfiguration)(cfg)
        cfg2 = deserialize(model.DHEConfiguration)(dct)
        dct2 = serialize(model.DHEConfiguration)(cfg2)
        self.assertEqual(dct, dct2)

    def test_units(self):
        u = model.Units["m"]
        self.assertTrue(u, model.Units.m)


if __name__ == '__main__':
    unittest.main()
