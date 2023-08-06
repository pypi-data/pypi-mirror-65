#ifndef _UTILS_H_
#define _UTILS_H_

#include <stdarg.h>
#include <stddef.h>
#include <setjmp.h>
#include <string.h>
#include <stdlib.h>
#include <math.h>
#include <cmocka.h>

#define DBL_EPSILON 1E-10
#define assert_double_almost_equal_prec(x, y, eps) assert_true((isnan(x) && isnan(y)) || fabs(x-(y)) <= eps)
#define assert_double_almost_equal(x, y) assert_double_almost_equal_prec(x, y, DBL_EPSILON)

void assert_array_almost_equal(double *x, double *y, unsigned int size);
void assert_array_almost_equal_prec(double *x, double *y, unsigned int size, double precision);
void assert_array_almost_equal_factor(double *x, double *y, double c, unsigned int size);
void convert_matrix(double *x, double **y, unsigned int n, unsigned int m);

#endif // _UTILS_H_
