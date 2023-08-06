#define UNIT_TESTING
#include <stdarg.h>
#include <stddef.h>
#include <setjmp.h>
#include <string.h>
#include <stdlib.h>
#include <math.h>
#include <cmocka.h>
#include "cmocka_utils.h"

#include "original/multiplizieren.c"
#include <c_dhe/c_dhe.c>
#include "helpers/T_soil_tensor_fill.c"

#define DIMAXI 2
#define DIMRAD 3
#define SIZEAXI (DimAxi + 1)

static void test_tsoil(void **state)
{
  int i,j,l;
  double T_soil[(DIMRAD+2)*DIMAXI];
  double T_soil_new[(DIMRAD+2)*DIMAXI];
  Matrix TEarth_data = {{ NAN },
			{ 3.3, 10.3, 10.3, 10.3, 10.3},
			{ 4.3, 11.3, 11.3, 11.3, 11.3}};
  Matrix TEarth_new_data;
  double T_soil_tensor[DIMRAD*(DIMRAD+2)*DIMAXI];
  KMatrix B_data =  {
    {{1.0, 0.0, 0.0, 0.0, 0.0},
     { 0.0 },
     { 0.0 },
     { 0.0 }},
    {{1.0, 0.0, 0.0, 0.0, 0.0},
     {3.33e-02, 9.58e-01, 7.97e-03, 1.34e-05, 5.26e-09},
     {2.42e-05, 1.42e-03, 9.95e-01, 3.35e-03, 1.31e-06},
     {8.64e-09, 5.08e-07, 7.10e-04, 9.98e-01, 7.84e-04}},
    {{1.0, 0.0, 0.0, 0.0, 0.0},
     {3.33e-02, 9.58e-01, 8.11e-03, 1.47e-05, 6.25e-09},
     {2.54e-05, 1.49e-03, 9.94e-01, 3.62e-03, 1.53e-06},
     {9.77e-09, 5.74e-07, 7.65e-04, 9.98e-01, 8.46e-04}}};
  double *B_ptr_ptr[DIMAXI+1][DIMRAD+1];
  double **B[DIMAXI+1];
  for(i=0; i<=DIMAXI; i++)
    {
      B[i] = &B_ptr_ptr[i][0];
      for(j=0; j<=DIMRAD; j++)
	B_ptr_ptr[i][j] = &B_data[i][j][0];
    }
  
  T_soil_tensor_fill(B, DIMAXI, DIMRAD, T_soil_tensor);
  l = 0;
  for(j=0; j<DIMRAD+2; j++)
    for(i=1; i<=DIMAXI; i++)
      T_soil[l++] = TEarth_data[i][j];
  
  T_soil_refresh(T_soil, T_soil_tensor, DIMAXI, DIMRAD);
  for(i=1; i<=DIMAXI; i++)
    multiplizieren(B_data,TEarth_data,TEarth_new_data,i,DIMRAD);
  l = 0;
  for(j=0; j<DIMRAD+2; j++)
    for(i=1; i<=DIMAXI; i++)
      T_soil_new[l++] = TEarth_new_data[i][j];
  assert_array_almost_equal(T_soil_new, T_soil, sizeof(T_soil_new)/sizeof(double));
}

#undef DIMAXI
#undef DIMRAD
#undef SIZEAXI
#define DIMAXI 1
#define DIMRAD 5
#define SIZEAXI (DimAxi + 1)

static void test_tsoil_2(void **state)
{
  int i,j,l;
  double T_soil[(DIMRAD+2)*DIMAXI];
  double T_soil_new[(DIMRAD+2)*DIMAXI];
  Matrix TEarth_data = {
    { NAN },
    {8.74435771, 11.3, 11.3, 11.3, 11.3, 11.3, 11.3} };
  Matrix TEarth_new_data;
  double T_soil_tensor[DIMRAD*(DIMRAD+2)*DIMAXI];
  KMatrix B_data =  {
    {{1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0},
     { 0.0 },
     { 0.0 },
     { 0.0 },
     { 0.0 },
     { 0.0 }},
    {{1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0},
     { 4.04804839e-01, 4.71896865e-01, 1.20053553e-01, 3.22436153e-03, 2.03498764e-05, 3.12523526e-08, 3.50040651e-11},
     { 5.90028078e-03, 2.14538067e-02, 9.20733367e-01, 5.15864680e-02, 3.25577091e-04, 5.00005496e-07, 5.60029037e-10},
     { 3.34854688e-05, 1.21755354e-04, 1.09006096e-02, 9.76451018e-01, 1.24739529e-02, 1.91568915e-05, 2.14565952e-08},
     { 4.90392187e-08, 1.78309806e-07, 1.59638612e-05, 2.89449774e-03, 9.94023556e-01, 3.06232460e-03, 3.42994370e-06},
     { 1.81752786e-11, 6.60865013e-11, 5.91664453e-09, 1.07278020e-06, 7.39039784e-04, 9.97023124e-01, 2.23675729e-03}}};
  double *B_ptr_ptr[DIMAXI+1][DIMRAD+1];
  double **B[DIMAXI+1];
  for(i=0; i<=DIMAXI; i++)
    {
      B[i] = &B_ptr_ptr[i][0];
      for(j=0; j<=DIMRAD; j++)
	B_ptr_ptr[i][j] = &B_data[i][j][0];
    }
  
  T_soil_tensor_fill(B, DIMAXI, DIMRAD, T_soil_tensor);
  l = 0;
  for(j=0; j<DIMRAD+2; j++)
    for(i=1; i<=DIMAXI; i++)
      T_soil[l++] = TEarth_data[i][j];
  
  T_soil_refresh(T_soil, T_soil_tensor, DIMAXI, DIMRAD);
  for(i=1; i<=DIMAXI; i++)
    multiplizieren(B_data,TEarth_data,TEarth_new_data,i,DIMRAD);
  l = 0;
  for(j=0; j<DIMRAD+2; j++)
    for(i=1; i<=DIMAXI; i++)
      T_soil_new[l++] = TEarth_new_data[i][j];
  assert_array_almost_equal(T_soil_new, T_soil, sizeof(T_soil_new)/sizeof(double));
}

static void test_tsoil_id(void **state)
{
  unsigned int i;
  double T_soil[(DIMRAD+2)*DIMAXI] = { 0., 1., 2., 3., 4.,
				       5., 6.};
  double T_soil_ref[(DIMRAD+2)*DIMAXI];
  for(i=0; i<sizeof(T_soil)/sizeof(double); i++)
    T_soil_ref[i] = T_soil[i];
  double T_soil_tensor[DIMRAD*(DIMRAD+2)*DIMAXI];
  T_soil_tensor_fill_id(DIMAXI, DIMRAD, T_soil_tensor);
  
  T_soil_refresh(T_soil, T_soil_tensor, DIMAXI, DIMRAD);
  assert_array_almost_equal(T_soil, T_soil_ref, sizeof(T_soil)/sizeof(double));
}

int main(void)
{
  const struct CMUnitTest tests[] = {
    cmocka_unit_test(test_tsoil),
    cmocka_unit_test(test_tsoil_id),
    cmocka_unit_test(test_tsoil_2),
    //    cmocka_unit_test(test_),
  };
  return cmocka_run_group_tests(tests, NULL, NULL);
}
