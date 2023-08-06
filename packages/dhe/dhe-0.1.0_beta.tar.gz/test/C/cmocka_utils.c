#include "cmocka_utils.h"

void assert_array_almost_equal(double *x, double *y, unsigned int size)
{
  unsigned int i;
  for(i=0; i<size; i++)
    assert_double_almost_equal(x[i], y[i]);
}
void assert_array_almost_equal_prec(double *x, double *y, unsigned int size, double eps)
{
  unsigned int i;
  for(i=0; i<size; i++)
    assert_double_almost_equal_prec(x[i], y[i], eps);
}
void assert_array_almost_equal_factor(double *x, double *y, double c, unsigned int size)
// x == y*c
{
  unsigned int i;
  for(i=0; i<size; i++)
    assert_double_almost_equal(x[i], c*y[i]);
}
