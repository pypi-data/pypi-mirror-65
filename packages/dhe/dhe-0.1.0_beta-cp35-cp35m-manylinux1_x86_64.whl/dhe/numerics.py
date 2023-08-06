import numpy
from scipy.linalg import solve_banded


def recursive_sequence(a, b, x0):
    """
    Computes the sequence
    x_{i+1} = a_i * x_i + b_i
    x_0 = x0
    """
    n = a.shape[0] + 1
    M = numpy.empty((2, n))
    M[0] = 1.
    M[1, :-1] = -a
    B = numpy.empty(n)
    B[1:] = b
    B[0] = x0
    return solve_banded((1, 0), M, B, overwrite_ab=True, overwrite_b=True)
