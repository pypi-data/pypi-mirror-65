#!/usr/bin/env python3

import unittest
import numpy

from dhe import numerics


def recursive_sequence_loop(a, b, x0):
    n = a.shape[0]
    x = numpy.empty(n + 1)
    x[0] = x0
    for i in range(n):
        x[i + 1] = a[i] * x[i] + b[i]
    return x


class TestNumerics(unittest.TestCase):
    a = numpy.array([1., 2., 3.])
    b = numpy.array([2., 1., -1.])
    x = numerics.recursive_sequence(a, b, 0.)
    x_ref = recursive_sequence_loop(a, b, 0.)

    numpy.testing.assert_array_almost_equal(x, x_ref)


if __name__ == '__main__':
    import timeit
    _a = numpy.array(numpy.ones(100))
    _b = numpy.array(numpy.ones(100))
    print(timeit.timeit(stmt="recursive_sequence_loop(a, b, 0.)",
                        setup="from __main__ import "
                        "recursive_sequence_loop, a, b",
                        number=100))
    print(timeit.timeit(stmt="recursive_sequence(a, b, 0.)",
                        setup="from dhe.numerics import recursive_sequence;"
                        " from __main__ import a, b",
                        number=100))
