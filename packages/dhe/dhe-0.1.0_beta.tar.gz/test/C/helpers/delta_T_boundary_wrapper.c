#include <c_dhe/c_dhe.c>

void Delta_T_boundary_1(double *g,
			unsigned int dim_t, unsigned int dim_ax,
			double *q,
			double *d_lambda_soil, double *T_out)
{
  DHE dhe = {.g = g, .d_lambda_soil = d_lambda_soil};
  DHE_config *config = dhe_config_new(&dhe, 1, dim_t, dim_ax);
  DHE_state states[] = {{.Q = q}};
  Delta_T_boundary(config, states, dim_t, dim_ax, T_out);
  dhe_config_destroy(config);
}
