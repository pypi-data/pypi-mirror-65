#ifndef __DHE_H__
#define __DHE_H__

typedef double (*T_brine_refresh_fun)(const double *T_soil, double *T_U, double *Q_wall,
				      unsigned int dim_ax,
				      double T_sink,
				      const void *parameters);

typedef struct {
  unsigned int n_sub_steps;
  double kappa_ax;
  double *kappa_rad;
  double *lambda_brine;
} T_brine_parameters;

typedef struct {
  double *T_soil_tensor;
  double *L;
  T_brine_refresh_fun T_brine_refresh;
  void *T_brine_parameters;
} T_soil_parameters;
// TODO: move T_brine_refresh out of T_soil_parameters
// TODO: redundant L

typedef struct
{
  double L;
  double R;
  double x, y;
  double *g;
  double *d_lambda_soil;
  unsigned int n_steps;
  double L1_on;
  T_soil_parameters pump_dependent_parameters[2];
} DHE;

typedef struct
{
  double *Q;
  double *T_soil;
  double *T_U;
  double T_sink;
} DHE_state;

double T_brine(const double *T_soil, double *T_U, double *Q_wall,
	       unsigned int dim_ax,
	       double T_sink,
	       const T_brine_parameters *parameters);

typedef struct {
  double *kappa_brine;
  double *kappa_soil;
  double *L;
}
  T_brine_stationary_parameters;

double T_brine_stationary(const double *T_soil, double *T_U, double *Q_wall,
			  unsigned int dim_ax,
			  double T_sink,
			  const T_brine_stationary_parameters *parameters);

typedef struct {
  double g_coefs[6];
  double u_min, L, go_const;
}
  g_func_parameters;

#define default_go_const 6.84

void g_func(const double *t, unsigned int dim_t,
	    const double* c_V_soil,
	    const double* lambda_soil,
	    unsigned int dim_ax,
	    const double *r,
	    unsigned int dim_rad,
	    double *out_g,
	    const g_func_parameters *prm
	    );

void g_cone(const double *t, unsigned int dim_t,
	    const double* c_V_soil,
	    const double* lambda_soil,
	    unsigned int dim_ax,
	    const double *r,
	    unsigned int dim_rad,
	    double *out_g,
	    const g_func_parameters *prm);


typedef struct {
  double *T_sink;
  double *T_source;
  double *T_soil;
} calc_P_output;

void calc_P(double *P, double *U_brine,
	    unsigned int dim_ax, unsigned int dim_rad,
	    unsigned int dim_t,
	    unsigned int n_DHE,
	    const DHE *dhe,
	    DHE_state *dhe_states,
	    double *sum_Q0,
	    double *Q_wall,
	    unsigned int n_boundary_refresh,
	    double precision,
	    calc_P_output *restrict out);

#endif // __DHE_H__
