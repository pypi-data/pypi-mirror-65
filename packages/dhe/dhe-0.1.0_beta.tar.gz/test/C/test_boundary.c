#define UNIT_TESTING
#include <stdarg.h>
#include <stddef.h>
#include <setjmp.h>
#include <string.h>
#include <stdlib.h>
#include <math.h>
#include <cmocka.h>
#include "cmocka_utils.h"

#include "original/rand.c"
#include "helpers/delta_T_boundary_wrapper.c"

#define DimAxi 2
#define DimRad 3
#define SizeAxi (DimAxi + 1)
#define dim_t 4

typedef struct {
  int Woche, RepRandBed;
  double c_p_soil, r, L;
  double rho_soil[SizeAxi];
  double c_V_soil[SizeAxi];
  double lambda_soil[SizeAxi];
  double d_lambda_soil[SizeAxi];
  double t[dim_t];
  double Q[(dim_t+1)*DimAxi];
  MatrixQ Q_pas;
  double Q1[dim_t+1];
  double Trt_ref[DimAxi];
} config;

config new_config()
{
  unsigned int i, j, l=0;
  config c = {
    .Woche = 4,
      .RepRandBed = 1,
      .c_p_soil = 1000.,
      .rho_soil = {2600, 2650.},
      .lambda_soil = {2.5, 1.5},
      .r = 1.5,
      .L = 100.,
      };
  for(i=0;i<DimAxi; i++)
    {
      c.c_V_soil[i] = c.c_p_soil * c.rho_soil[i];
      c.d_lambda_soil[i] = c.lambda_soil[i] * c.L / DimAxi;
    }
  for(i=0;i<dim_t; i++)
    c.t[i] = (i+1) * 604800 * c.RepRandBed;
  for(i=0; i<sizeof(c.Q)/sizeof(double); i++)
    c.Q[i] = i*i;
  for(i=0; i<dim_t+1; i++)
    c.Q1[i] = c.Q[i*DimAxi];
  for(i=0; i<dim_t+1; i++)
    for(j=0; j<DimAxi; j++)
      c.Q_pas[j+1][i] = c.Q[l++];
  
  return c;
}

static void test_boundary(void **state)
{
  int k;
  config c = new_config();
  double g[dim_t*DimAxi];
  double T_out[DimAxi] = {0., 0.};
  for(k=0; k<DimAxi; k++)
    c.Trt_ref[k] = RandAussen(k+1, c.Woche,
			      0., 0,
			      c.RepRandBed,
			      c.Q_pas,
			      c.c_p_soil,
			      c.rho_soil[k],
			      c.lambda_soil[k],
			      c.r, c.L,
			      DimAxi);
  g_cone(c.t, dim_t, c.c_V_soil, c.lambda_soil, 1, &c.r, 1, g, NULL);
  Delta_T_boundary_1(g, dim_t, 1, c.Q1, c.d_lambda_soil, T_out);
  assert_array_almost_equal_prec(T_out, c.Trt_ref, 1, 1.E-5);

  T_out[0] = T_out[1] = 0.;
  g_cone(c.t, dim_t, c.c_V_soil, c.lambda_soil, DimAxi, &c.r, 1, g, NULL);
  Delta_T_boundary_1(g, dim_t, DimAxi, c.Q, c.d_lambda_soil, T_out);
  assert_array_almost_equal_prec(T_out, c.Trt_ref, DimAxi, 1.E-5);
}

static void test_boundary_gfunc(void **state)
{
  int k;
  config c = new_config();
  double g[dim_t*DimAxi];
  double T_out[DimAxi] = {0., 0.};
  g_func_parameters prm = {
    .g_coefs = {0.1, 0.3, -0.2, 0.11, -0.001, 0.5},
    .u_min = 0.5,
    .go_const = default_go_const,
    .L = c.L
  };
  const double *c_g = prm.g_coefs;
  for(k=0; k<DimAxi; k++)
    c.Trt_ref[k] = RandAussen_gfunc(k+1, c.Woche,
				    0., 0,
				    c.RepRandBed,
				    c.Q_pas,
				    c.c_p_soil,
				    c.rho_soil[k],
				    c.lambda_soil[k],
				    c.r, c.L,
				    c_g[0], c_g[1], c_g[2], c_g[3], c_g[4], c_g[5],
				    DimAxi,
				    prm.u_min);
  g_func(c.t, dim_t, c.c_V_soil, c.lambda_soil, 1, &c.r, 1, g, &prm);
  Delta_T_boundary_1(g, dim_t, 1, c.Q1, c.d_lambda_soil, T_out);
  assert_array_almost_equal(T_out, c.Trt_ref, 1);

  T_out[0] = T_out[1] = 0.;
  g_func(c.t, dim_t, c.c_V_soil, c.lambda_soil, DimAxi, &c.r, 1, g, &prm);
  Delta_T_boundary_1(g, dim_t, DimAxi, c.Q, c.d_lambda_soil, T_out);
  assert_array_almost_equal(T_out, c.Trt_ref, DimAxi);
}


int main(void)
{
  const struct CMUnitTest tests[] = {
    cmocka_unit_test(test_boundary),
    cmocka_unit_test(test_boundary_gfunc),
    //    cmocka_unit_test(test_),
  };
  return cmocka_run_group_tests(tests, NULL, NULL);
}
