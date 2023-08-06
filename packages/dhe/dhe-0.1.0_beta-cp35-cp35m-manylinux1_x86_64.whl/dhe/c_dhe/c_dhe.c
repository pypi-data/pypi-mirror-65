#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
#include "c_dhe.h"

typedef struct
{
  double *sum_g, *dg;
  unsigned int n_DHE;
  const DHE *dhe;
} DHE_config;


double mean(double *x, unsigned int n);
double soil_step(double *T_soil, double T_sink, double *sum_Q0,
		 unsigned int dim_ax, unsigned int dim_rad,
		 unsigned int n_steps,
		 double *Q_wall, double *T_U,
		 const T_soil_parameters *pump_dependent_parameters);
void Delta_T_boundary(const DHE_config *dhe_config, const DHE_state *states, unsigned int dim_t, unsigned int dim_ax, double *restrict T_out);

void boundary_step(const double *P,
		   const double *U_brine,
		   unsigned int dim_ax, unsigned int dim_rad,
		   unsigned int n_steps,
		   double U1_on,
		   const T_soil_parameters* pump_dependent_parameters,
		   double *T_sink_p,
		   double *T_soil, double *T_U, double *sum_Q0,
		   double *Q_wall,
		   unsigned int n_boundary_refresh,
		   double *T_soil_old,
		   double *T_U_old,
		   double *sum_Q0_old,
		   double precision,
		   calc_P_output *restrict out);
static DHE_config* dhe_config_new(const DHE *dhe, unsigned int n_DHE,
				  unsigned int dim_t, unsigned int dim_ax);

static void dhe_config_destroy(DHE_config* config);

typedef struct
{
  const double *P;
  const double *U_brine;
  calc_P_output *out;
  double **Q;
  unsigned int n_DHE;
  size_t size, rest_size;
  unsigned int pos;
} io_chunk;
static void io_chunk_init(io_chunk *chunk, unsigned int n_DHE,
			  const double *P,
			  const double *U_brine,
			  DHE_state *dhe_states,
			  calc_P_output *out,
			  size_t chunk_size,
			  size_t total_size)
{
  unsigned int k;
  chunk->P = P;
  chunk->U_brine = U_brine;
  chunk->n_DHE = n_DHE;
  chunk->out = malloc(n_DHE*sizeof(calc_P_output));
  chunk->Q = malloc(n_DHE*sizeof(double*));
  for(k=0; k<n_DHE; k++)
    {
      chunk->out[k] = out[k];
      chunk->Q[k] = dhe_states[k].Q;
    }
  if(chunk_size > total_size) chunk_size = total_size;
  chunk->size = chunk_size;
  chunk->rest_size = total_size - chunk_size;
  chunk->pos = 0;
}
static void io_chunk_finalize(io_chunk *chunk)
{
  free(chunk->out);
  free(chunk->Q);
}
static _Bool io_chunk_next(io_chunk *chunk, size_t size_T_soil, unsigned int dim_ax)
{
  unsigned int i;
  size_t step = chunk->size;
  if(chunk->rest_size == 0) return false;
  chunk->P += step;
  chunk->U_brine += step;
  for(i=0; i<chunk->n_DHE; i++)
    {
      chunk->out[i].T_sink += step;
      chunk->out[i].T_source += step;
      chunk->out[i].T_soil += step*size_T_soil;
      chunk->Q[i] += dim_ax;
    }
  if(chunk->rest_size <= chunk->size)
    chunk->size = chunk->rest_size;
  chunk->rest_size -= chunk->size;
  chunk->pos++;
  return true;
}

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
	    calc_P_output *restrict out)
/**
 * @param U_brine U_brine = Phi_m * c_brine [W/K]
 */
{
  unsigned int j, k;
  double *T_soil_old = malloc(dim_ax*(dim_rad+2)*sizeof(double));
  double *T_U_old = malloc(2*dim_ax*sizeof(double));
  double *sum_Q0_old = malloc(dim_ax*sizeof(double));
  double *T0 = malloc(n_DHE * dim_ax * sizeof(double));
  double *T_soil_boundary = NULL;
  for(k=0; k<n_DHE; k++)
    {
      memcpy(&T0[k*dim_ax], &dhe_states[k].T_soil[dim_rad*dim_ax], dim_ax*sizeof(double));
      dhe_states[k].T_sink = mean(&dhe_states[k].T_soil[dim_ax], dim_ax);
    }
  unsigned int N = dim_t / n_boundary_refresh;
  if(dim_t % n_boundary_refresh != 0) N++;
  io_chunk chunk;
  DHE_config *dhe_config = dhe_config_new(dhe, n_DHE, N, dim_ax);
  io_chunk_init(&chunk, n_DHE, P, U_brine, dhe_states, out, n_boundary_refresh, dim_t);
  while(true)
    {
      for(k=0; k<n_DHE; k++)
	boundary_step(chunk.P,
		      chunk.U_brine,
		      dim_ax, dim_rad,
		      dhe[k].n_steps,
		      dhe[k].L1_on*n_DHE,
		      dhe[k].pump_dependent_parameters,
		      &dhe_states[k].T_sink,
		      dhe_states[k].T_soil, dhe_states[k].T_U,
		      sum_Q0,
		      Q_wall,
		      chunk.size,
		      T_soil_old,
		      T_U_old,
		      sum_Q0_old,
		      precision,
		      &chunk.out[k]
		      );
      if(!io_chunk_next(&chunk, dim_ax*(dim_rad+2), dim_ax)) break;
      for(k=0; k<n_DHE; k++)
	{
	  T_soil_boundary = &dhe_states[k].T_soil[dim_ax*(dim_rad+1)];
	  for(j=0; j<dim_ax; j++)
	    {
	      chunk.Q[k][j] = sum_Q0[j] / (dhe[k].n_steps * n_boundary_refresh);
	      T_soil_boundary[j] = T0[k*dim_ax + j];
	      sum_Q0[j] = 0.;
	    }
	}
      Delta_T_boundary(dhe_config,
		       dhe_states,
		       chunk.pos, dim_ax,
		       T_soil_boundary);
    }
  free(T_soil_old);
  free(T_U_old);
  free(sum_Q0_old);
  free(T0);
  io_chunk_finalize(&chunk);
  dhe_config_destroy(dhe_config);
}

void boundary_step(const double *P,
		   const double *U_brine,
		   unsigned int dim_ax, unsigned int dim_rad,
		   unsigned int n_steps,
		   double U1_on,
		   const T_soil_parameters* pump_dependent_parameters,
		   double *T_sink_p,
		   double *T_soil, double *T_U, double *sum_Q0,
		   double *Q_wall,
		   unsigned int n_boundary_refresh,
		   double *T_soil_old,
		   double *T_U_old,
		   double *sum_Q0_old,
		   double precision,
		   calc_P_output *restrict out)
/**
 * U1_on = L1_on * n_DHE
 */
{
  unsigned int i;
  _Bool pump_is_on;
  double T_source, T_sink_ref;
  double T_sink = *T_sink_p;

  for(i=0; i<n_boundary_refresh; i++)
    {
      pump_is_on = U_brine[i] > 0.;
      if(pump_is_on)
	{
	  T_sink -= P[i] * (1. / U1_on + 1. / U_brine[i]);
	  memcpy(T_soil_old, T_soil, dim_ax*(dim_rad+2)*sizeof(double));
	  memcpy(T_U_old, T_U, 2*dim_ax*sizeof(double));
	  memcpy(sum_Q0_old, sum_Q0, dim_ax*sizeof(double));
	}
      T_source = soil_step(T_soil, T_sink,
			   sum_Q0, dim_ax, dim_rad,
			   n_steps,
			   Q_wall,
			   T_U,
			   &pump_dependent_parameters[pump_is_on]);
      if(pump_is_on)
	{
	  T_sink = T_source - P[i] / U_brine[i];
	  T_sink_ref = T_sink + 2*precision;
	  while(fabs(T_sink - T_sink_ref) > precision)
	    {
	      memcpy(T_soil, T_soil_old, dim_ax*(dim_rad+2)*sizeof(double));
	      memcpy(T_U, T_U_old, 2*dim_ax*sizeof(double));
	      memcpy(sum_Q0, sum_Q0_old, dim_ax*sizeof(double));
	      T_source = soil_step(T_soil, T_sink,
				   sum_Q0, dim_ax, dim_rad,
				   n_steps,
				   Q_wall,
				   T_U,
				   &pump_dependent_parameters[pump_is_on]);
	      T_sink_ref = T_sink;
	      T_sink = T_source - P[i] / U_brine[i];
	      if(fabs(T_sink) > 100)
		{
		  T_sink = -1.;
		  T_sink_ref = T_sink + 2*precision;
		}
	    }
	}
      else
	{
	  T_sink = T_soil[dim_ax+1];
	  T_source = T_sink;
	}
      out->T_sink[i] = T_sink;
      out->T_source[i] = T_source;
      memcpy(&out->T_soil[i*dim_ax*(dim_rad+2)], T_soil, dim_ax*(dim_rad+2)*sizeof(double));
    }
  *T_sink_p = T_sink;
}

void Delta_T_boundary(const DHE_config *dhe_config, const DHE_state *states, unsigned int dim_t, unsigned int dim_ax, double *restrict T_out)
/**
 * @brief Superposition of boundary conditions
 *
 * @param d_lamda_soil lambda_soil * dl. shape: (dim_ax,) or ()
 * @param q Heat loss. shape: (dim_t+1, dim_ax)
 * @param g Values of the g function per time and height. shape: (dim_t, dim_ax)
 */
{
  unsigned int i, j, k;
  double Delta_T;
  const double *sum_g = dhe_config->sum_g, *dg = dhe_config->dg;
  const DHE *dhe = dhe_config->dhe;
  
  for(j=0; j<dim_ax; j++)
    {
      Delta_T = 0.;
      for(k=0; k<dhe_config->n_DHE; k++)
	{
	  for(i=0;i<dim_t; i++)
	    Delta_T += (sum_g[i*dim_ax+j] - dg[k]) * (-states[k].Q[(dim_t-i)*dim_ax+j] + states[k].Q[(dim_t-1-i)*dim_ax+j]);
	  T_out[k*dim_ax + j] += Delta_T/(2 * M_PI * dhe[k].d_lambda_soil[j]);
	}
    }
}
static void DHE_geometry(const DHE *dhe, unsigned int n_DHE, double *restrict out_dg)
/**
 * @brief Encodes the distances between the single DHEs into an array out_dg
 *        for use in Delta_T_boundary
 *
 * out_dg[k] = \sum_{l=0, l\neq k}^n_DHE log(d(k,l)/r[l]), where
 * d(k, l) is the distance between dhe k and dhe l.
 *
 * g_eff[k] = g[k] + \sum_{l=0, l\neq k}^n_DHE g[l] - log(d(k, l)/r[l])
 *          = \sum_{l=0}^n_DHE g[l] - \sum_{l=0, l\neq k}^n_DHE log(d(k, l)/r[l])
 */
{
  unsigned int k, l;
  for(k=0; k<n_DHE; k++)
    {
      out_dg[k] = 0.;
      for(l=0; l<n_DHE; l++)
	{
	  if(l == k) continue;
	  out_dg[k] += log(hypot(dhe[k].x - dhe[l].x, dhe[k].y - dhe[l].y)/dhe[l].R);
	}
    }
}
static void sum_g(const DHE *dhe, unsigned int n_DHE, unsigned int size_g, double *restrict out_sum_g)
{
  unsigned int k, l;
  for(l=0; l<size_g; l++)
    {
      out_sum_g[l] = 0.;
      for(k=0; k<n_DHE; k++)
	out_sum_g[l] += dhe[k].g[l];
    }
}
static DHE_config* dhe_config_new(const DHE *dhe, unsigned int n_DHE,
				  unsigned int dim_t, unsigned int dim_ax)
{
  DHE_config* dhe_config = malloc(sizeof(DHE_config));
  *dhe_config = (DHE_config){.sum_g = malloc(dim_t * dim_ax * sizeof(double)),
			     .dg = malloc(n_DHE * sizeof(double)),
			     .n_DHE = n_DHE, .dhe = dhe};
  sum_g(dhe, n_DHE, dim_t * dim_ax, dhe_config->sum_g);
  DHE_geometry(dhe, n_DHE, dhe_config->dg);
  return dhe_config;
}

static void dhe_config_destroy(DHE_config* config)
{
  free(config->sum_g);
  free(config->dg);
  free(config);
}

double T_brine(const double *T_soil, double *restrict T_U, double *restrict Q_wall,
	       unsigned int dim_ax,
	       double T_sink,
	       const T_brine_parameters *parameters)
/**
 * @param Q_wall passed only to prevent reallocating [W/m]
 * @param U_brine U_brine = Phi c_V_brine
 * @param dC_brine dC_brine = 2 c_V_brine pi r_DHE^2 dl
 * @param kappa_ax kappa_ax = U_brine / dC_brine * dt_step
 * @param kappa_rad kappa_rad = lambda_brine * dt / dC_brine
 * @param lambda_brine lambda_brine = 0.5 * L / n_sub_steps
 */
{
  // double dt_step = dt / n_sub_steps;
  double T_out = 0;
  // double L0mcpdt = U_brine / dC_brine * dt_step;
  // lambda_brine = 0.5 * L / n_sub_steps;
  // double L1mcpdt = lambda_brine * dt / dC_brine;
  unsigned int i, _step;
  for(i=0;i<dim_ax; i++)
    Q_wall[i] = 2 * parameters->n_sub_steps * T_soil[i];
  double *T_up = &T_U[dim_ax];
  double kappa_ax = parameters->kappa_ax;
  double *kappa_rad = parameters->kappa_rad;
  double T_prev;
  for(_step=0;_step<parameters->n_sub_steps;_step++)
    {
      T_prev = T_sink;
      for(i=0; i<dim_ax; i++) {
	T_U[i] += (T_prev - T_U[i]) * kappa_ax + (T_soil[i] - T_U[i]) * kappa_rad[i];
	T_prev = T_U[i];
      }
      for(i=0; i<dim_ax; i++) {
	T_up[i] += (T_prev - T_up[i]) * kappa_ax + (T_soil[dim_ax - 1 - i] - T_up[i]) * kappa_rad[dim_ax - 1 - i];
	T_prev = T_up[i];
      }
      for(i=0; i<dim_ax; i++)
	Q_wall[i] -= (T_U[i] + T_up[dim_ax-1-i]);
      T_out += T_up[dim_ax-1];
    }
  for(i=0; i<dim_ax; i++)
    Q_wall[i] *= parameters->lambda_brine[i];
  T_out /= parameters->n_sub_steps;
  return T_out;
}

double T_brine_stationary(const double *T_soil, double *restrict T_U, double *restrict Q_wall,
	       unsigned int dim_ax,
	       double T_sink,
	       const T_brine_stationary_parameters *parameters)
/**
 * @brief Static T_brine method
 *
 * @param U_brine U_brinemcpdt = U_brine / U_brine * dt2
 * @param T_U shape (2, n)
 * T_U[0] is T_down, T_U[1] is T_up
 * kappa_soil = L / (L + 2*U_brine)
 * kappa_brine = U_brine / (0.5 * L + U_brine)
 */
{
  unsigned int i;
  const double *kappa_soil = parameters->kappa_soil;
  const double *kappa_brine = parameters->kappa_brine;
  double *T_up = &T_U[dim_ax];
  T_U[0] = kappa_soil[0] * T_soil[0] + kappa_brine[0] * T_sink;
  for(i=1; i<dim_ax; i++)
    T_U[i] = kappa_soil[i] * T_soil[i] + kappa_brine[i] * T_U[i - 1];
  for(i=0; i<dim_ax; i++)
    T_up[i] = kappa_soil[dim_ax-1-i] * T_soil[dim_ax-1-i] + kappa_brine[dim_ax-1-i] * T_up[(int)i-1];
  for(i=0; i<dim_ax; i++)
    Q_wall[i] = (2 * T_soil[i] - T_U[i] - T_up[dim_ax-1-i]) * 0.5 * parameters->L[i];

  return T_up[dim_ax-1];
}

void T_soil_refresh(double *restrict T_soil, const double* T_soil_tensor, unsigned int dim_ax, unsigned int dim_rad);

double soil_step(double *restrict T_soil,
		 double T_sink, double *restrict sum_Q0,
		 unsigned int dim_ax, unsigned int dim_rad,
		 unsigned int n_steps,
		 double *restrict Q_wall, double *restrict T_U,
		 const T_soil_parameters *pump_dependent_parameters)
/**
 * @param U_brine U_brine = cp_brine * Phi_m / n_DHE
 * @param T_soil shape: (dim_rad+2, dim_ax)
 */
{
  unsigned int _, i;
  //B, L, T_brine_refresh = pump_dependent_parameters[U_brine > 0.]
  //T_s = U_brine and T_sink
  double T_source = 0.;
  double *T_soil_1 = &T_soil[dim_ax];
  for(_=0; _<n_steps; _++)
    {
      // Calculate brine Temperature
      T_source += (*pump_dependent_parameters->T_brine_refresh)(T_soil_1, T_U, Q_wall, dim_ax, T_sink, pump_dependent_parameters->T_brine_parameters);
      for(i=0; i<dim_ax; i++)
	{
	  T_soil[i] = T_soil_1[i] - Q_wall[i] / pump_dependent_parameters->L[i];
	  sum_Q0[i] += Q_wall[i];
	}
      // Update soil temperature
      T_soil_refresh(T_soil, pump_dependent_parameters->T_soil_tensor, dim_ax, dim_rad);
    }
  T_source /= n_steps;
  return T_source;
}

void T_soil_refresh(double *restrict T_soil, const double* T_soil_tensor, unsigned int dim_ax, unsigned int dim_rad)
/**
 * @param T_soil [dim_rad+2, dim_ax]
 * @param T_soil_tensor [dim_rad, dim_rad+2, dim_ax]
 * sum_j TT_kij T_kj --> sum_j TT_ijk T_jk
 */
{
  unsigned int i, j, k, stride = dim_ax * (dim_rad+2);
  double *x = malloc((dim_rad)*sizeof(double));
  double *T_soil_out = &T_soil[dim_ax];
  for(j=0; j<dim_ax; j++)
    {
      for(i=0; i<dim_rad; i++)
	{
	  x[i] = 0.;
	  for(k=0; k<dim_rad+2; k++)
	    x[i] += T_soil_tensor[stride*i + dim_ax*k + j] * T_soil[dim_ax*k + j];
	}
      for(i=0; i<dim_rad; i++)
	T_soil_out[dim_ax*i + j] = x[i];
    }
  free(x);
}
__inline__ double mean(double *x, unsigned int n)
{
  double m = 0.;
  while(n != 0)
    m += x[--n];
  return m;
}

void g_func(const double *t, unsigned int dim_t,
	    const double* c_V_soil,
	    const double* lambda_soil,
	    unsigned int dim_ax,
	    const double *r,
	    unsigned int dim_rad,
	    double *out_g,
	    const g_func_parameters *prm
	    )
/**
 * @brief Boundary condition with g function
 * 
 * @param t Array of time [s]
 * @param c_V_soil Volume specific heat of soil
 * @param L Length of borehole
 * @param r Radius at which to calculate boundary conditions
 */
{
  double u, g, go;
  unsigned int i, j, k, l=0;
  double L = prm->L, u_min = prm->u_min, go_const = prm->go_const;
  const double *g_coefs = prm->g_coefs;
  double *ts = malloc(dim_ax * sizeof(double));
  double *log_r = malloc(dim_rad * sizeof(double));
  for(i=0; i<dim_ax; i++)
    ts[i] = L*L/(9*lambda_soil[i]) * c_V_soil[i]; 
  for(j=0; j<dim_rad; j++)
    log_r[j] = log(r[j]/(L*0.0005));
  for(k=0; k<dim_t; k++)
    for(i=0; i<dim_ax; i++)
      {
	u = log(t[k] / ts[i]);
	if(u > 2.5) u = 2.5;
	go = 0.5*u + go_const;
	if(u < u_min) g = go;
	else g = g_coefs[0] + u*(g_coefs[1] + u*(g_coefs[2] + u*(g_coefs[3] + u*(g_coefs[4] + u*g_coefs[5]))));
	if(u < -2 && go - 0.3 > g) g = go;
	for(j=0; j<dim_rad; j++)
	  out_g[l++] = g - log_r[j];
      }
  free(ts);
  free(log_r);
}
void g_cone(const double *t, unsigned int dim_t,
	    const double* c_V_soil,
	    const double* lambda_soil,
	    unsigned int dim_ax,
	    const double *r,
	    unsigned int dim_rad,
	    double *out_g,
	    const g_func_parameters *prm)
/**
 *@brief Boundary condition according to cone formula by Werner
 */
{
  double u,_u, W,delta;
  unsigned int i, j, k, l=0, n;
  long fac;
  short sign;
  double *u0 = malloc(dim_ax * sizeof(double));
  double *rr = malloc(dim_rad * sizeof(double));
  _Bool keep_going;
  for(i=0; i<dim_rad; i++)
    rr[i] = r[i]*r[i];
  for(i=0; i<dim_ax; i++)
    u0[i] = c_V_soil[i] / (4 * lambda_soil[i]);
  for(k=0; k<dim_t; k++)
    for(i=0; i<dim_ax; i++)
      for(j=0; j<dim_rad; j++)
	{
	  u = u0[i]*rr[j] / t[k];
	  if(u > 1) W = 0;
	  else
	    {
	      W = -0.5772 - log(u) + u;
	      n = 1;
	      fac = 1;
	      sign = 1;
	      _u = u;
	      keep_going = 1;
	      while(keep_going)
		{
		  sign = -sign;
		  _u *= u;
		  n++;
		  fac *= n;
		  delta = _u / (fac * n);
		  keep_going = delta > 0.01 * fabs(W);
		  W += sign * delta;
		}
	      W *= 0.5;
	    }
	  out_g[l++] = W;
	}
  free(u0);
  free(rr);
}
