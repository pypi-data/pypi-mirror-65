#define UNIT_TESTING
#include <stdarg.h>
#include <stddef.h>
#include <setjmp.h>
#include <string.h>
#include <stdlib.h>
#include <math.h>
#include <cmocka.h>
#include "cmocka_utils.h"

#include <c_dhe/c_dhe.c>

#define DIM_RAD 5
#define DIM_AX 1
#define DIM_T 3

static void test_calc_P(void **state)
{
  double P[] = {500., 500., 500.};
  double U_brine[] = {1550, 1550, 1550};
  unsigned int dim_ax = DIM_AX;
  unsigned int dim_rad = DIM_RAD;
  unsigned int dim_t = DIM_T;
  unsigned int n_DHE = 1;
  unsigned int n_boundary_refresh = 168;
  double precision = 0.050000000000000003;
  double T_soil_tensor_off[] = {
    0.59397874051346522, 0.29734488581162227, 0.10581642441735493, 
    0.0028419850922479966, 1.7936588314892776e-05, 2.7546141825400331e-08, 
    3.0852939451901944e-11, 0.008657607331667273, 0.018909603709712432, 
    0.9205258518791879, 0.051580894651949261, 0.00032554191603941575, 
    4.9995147526961115e-07, 5.5996853182390063e-10, 4.913393965609493e-05, 
    0.00010731640879521776, 0.010899431875253459, 0.97645098670797781, 
    0.012473952720527192, 1.9156891195282716e-05, 2.1456594824823218e-08, 
    7.1956287394426816e-08, 1.5716407858714374e-07, 1.5962136517876929e-05, 
    0.0028944976978436932, 0.99402355649857899, 0.003062324602995571, 
    3.4299436980016677e-06, 2.6668972346233207e-11, 5.8249315208366271e-11, 
    5.9160052970580311e-09, 1.072780181624656e-06, 0.00073903978389686911, 
    0.99702312414521688, 0.0022367572897808168};
  double T_soil_tensor_on[] =  {
    0.4048048394700921, 0.47189686458986663, 0.12005355324199483, 
    0.0032243615342685116, 2.034987642134459e-05, 3.1252352576230658e-08, 
    3.5004065101952753e-11, 0.0059002807795125369, 0.021453806705801489, 
    0.9207333668329849, 0.051586468024971056, 0.00032557709120542555, 
    5.0000549558242791e-07, 5.6002903704641342e-10, 3.3485468752341334e-05, 
    0.00012175535384016725, 0.01090060957098705, 0.97645101833816916, 
    0.012473952920154458, 1.9156891501860582e-05, 2.1456595168204463e-08, 
    4.9039218714098792e-08, 1.78309805687369e-07, 1.5963861244476553e-05, 
    0.0028944977441658715, 0.9940235564988712, 0.0030623246029960194, 
    3.4299436980021704e-06, 1.8175278563197203e-11, 6.6086501251410785e-11, 
    5.9166445280085962e-09, 1.0727801987929248e-06, 0.00073903978389697742, 
    0.99702312414521688, 0.0022367572897808168};
  double L_off[] = {4523.7301988752424};
  double L_on[] = {2717.3748643622798};
  T_brine_parameters prm_off = {
	.n_sub_steps = 26,
	.kappa_ax = 0,
	.kappa_rad = (double[]){0.12081393309520569}, 
	.lambda_brine = (double[]){86.994811516831589}};
  T_brine_parameters prm_on = {
	.n_sub_steps = 16,
	.kappa_ax = 0.13453503219940435,
	.kappa_rad = (double[]){0.11792971447575207},
	.lambda_brine = (double[]){84.917964511321244}};

  double T_soil[] = {11.300000000000001, 11.300000000000001, 11.300000000000001, 
  11.300000000000001, 11.300000000000001, 11.300000000000001, 
		     11.300000000000001};
  double T_U[] = {0.87918606690479428, 0.87918606690479428};
  double sum_Q0[] = {0.5};
  double Q_wall[] = {0.};
  double Q[] = {0, 0.00027482746658799145, 8.6957128100106682e-05};
  double d_lambda_soil[] = {200.};
  double g[] = {0.22507230641451292, 0.34866754443584563, 0.45005589230285686};
  double out_T_sink[dim_t];
  double out_T_source[dim_t];
  double out_T_soil[dim_t*dim_ax*(dim_rad+2)];
  DHE dhe[] = {{.d_lambda_soil = d_lambda_soil, .g = g,
		.pump_dependent_parameters = {
	{.T_soil_tensor = T_soil_tensor_off,
	 .L = L_off,
	 .T_brine_refresh = (T_brine_refresh_fun)&T_brine,
	 .T_brine_parameters = &prm_off},
	{.T_soil_tensor = T_soil_tensor_on,
	 .L = L_on,
	 .T_brine_refresh = (T_brine_refresh_fun)&T_brine,
	 .T_brine_parameters = &prm_on}},
		.L1_on = 2717.3748643622798,
    .n_steps = 6}};
  DHE_state dhe_states[] = {{.T_soil = T_soil, .T_U = T_U, .Q = Q}};
  calc_P_output out = {.T_sink = out_T_sink, .T_source = out_T_source, .T_soil = out_T_soil};
  calc_P(P, U_brine, dim_ax, 
	 dim_rad, dim_t, n_DHE,
	 dhe,
	 dhe_states,
	 sum_Q0,
	 Q_wall,
	 n_boundary_refresh,
	 precision,
	 &out);

  double T_sink_ref[] =   {9.300160858675422304,  9.723971476460661734,  9.819883852268217694};
  double T_source_ref[] = {9.622741503836712340,  10.04655212162195177, 10.14246449742950773};
  double T_soil_ref[DIM_T][DIM_RAD+2] = {
    { 9.81202450206,  10.13546875734,  11.14439970418,  11.29489380946,
      11.29997040295,  11.29999996671,  11.3 },
    { 10.01618410089,  10.25686527103,  11.04916163617,  11.28212369308,
      11.29977835342,  11.29999949003,  11.3 },
    { 10.09481789394,  10.30753833297,  10.99858288058,  11.26659668638,
      11.29934322798,  11.29999764987,  11.3 }};
  assert_array_almost_equal(out_T_sink, T_sink_ref, dim_t);
  assert_array_almost_equal(out_T_source, T_source_ref, dim_t);
  assert_array_almost_equal(out_T_soil, T_soil_ref[0], dim_t*dim_ax*(dim_rad+2));
}


int main(void)
{
  const struct CMUnitTest tests[] = {
    cmocka_unit_test(test_calc_P),
    //    cmocka_unit_test(test_),
  };
  return cmocka_run_group_tests(tests, NULL, NULL);
}
