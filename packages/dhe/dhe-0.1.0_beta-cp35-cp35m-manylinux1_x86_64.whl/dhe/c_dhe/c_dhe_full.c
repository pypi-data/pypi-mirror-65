#include <stdlib.h>

#include "c_dhe_full.h"

double T_brine_stationary(void* self,
			  double *T_soil,
			  double *T_U,
			  double *Q_wall,
			  unsigned int dim_ax,
			  double T_sink) {
  return 0.;
}
double T_brine_dynamic(void* self,
		       double *T_soil,
		       double *T_U,
		       double *Q_wall,
		       unsigned int dim_ax,
		       double T_sink) {
  return 0.;
}

void calc_P_2(double *t, double *P, unsigned int dim_t, DHE2 *dhe, unsigned int n_DHE, GlobalParameters *env, double precision, CalcPOutput *out)
{
  return;
}

void free_global_parameters(GlobalParameters *env) {
  if(env != NULL) {
    if(env->soil_layers != NULL) free(env->soil_layers);
    if(env->g_method.data != NULL) free(env->g_method.data);
    free(env);
  }
}
