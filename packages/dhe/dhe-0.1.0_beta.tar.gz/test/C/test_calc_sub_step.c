#define UNIT_TESTING
#include <stdarg.h>
#include <stddef.h>
#include <setjmp.h>
#include <string.h>
#include <stdlib.h>
#include <math.h>
#include <cmocka.h>
#include "cmocka_utils.h"

#include "original/calculateEWS.c"
#include "helpers/T_soil_tensor_fill.c"
#include "helpers/delta_T_boundary_wrapper.c"

#define DIMAXI 3
#define DimRad 5
#define DimT 10
#define SizeAxi (DIMAXI + 1)


double *T_soil_tensor_new(unsigned int dim_ax, unsigned int dim_rad);
double *T_soil_tensor_new_from_pas(double ***B, unsigned int dim_ax, unsigned int dim_rad);
double *T_U_from_pas(double *TDown, double *TUp, unsigned int dim_ax);
T_brine_static_parameters T_brine_static_parameters_create(double *L_pas, unsigned int dim_ax, double L0);
void T_brine_static_parameters_free(T_brine_static_parameters* prm);
T_brine_parameters T_brine_parameters_create(double *L_pas, unsigned int dim_ax, unsigned int substep, double L0, double mcpSole, double dt);
void T_brine_parameters_free(T_brine_parameters* prm);
double* t_range(unsigned int dim_t, double dt, unsigned int i0);


typedef struct {
  int Iteration; int DimAxi; int DimRad_;
  int MonitorAxi;
  int MonitorRad;
  Matrix TEarthOld;
  Matrix TEarth;
  double TUp[DIMAXI+1];
  double TUpOld[DIMAXI+1];
  double TDownOld[DIMAXI+1];
  double TDown[DIMAXI+1];
  double Q0Old[DIMAXI+1];
  double Q0[DIMAXI+1];
  double TSourceOld;
  double TSource;
  double TSourceMin;
  double TSourceMax;
  double TSink;
  double TSinkMin;
  double TSinkMax;
  double QSource;
  double Massenstrom;
  double cpSole;
  double p;
  _Bool laminar;
  _Bool readFile;
  int simstep;
  int StepWrite;
  _Bool einschwingen;
  _Bool Allsteps;
  _Bool writeFile;
  _Bool Leistung;
  _Bool gfunction;
  int RepRandbed;
  int Zeitschritt;
  int Jahr;
  long numrows;
  _Bool Starttemp; 
  double DeltaT;
  int subdt;
  int AnzahlSonden;
  double Rechenradius;
  _Bool Stationaer;
  double mcpSole;
  int substep_run;
  double L1run[DIMAXI+1];
  int substep_stop;
  double L1stop[DIMAXI+1];
  double lambdaErde[DIMAXI+1];
  double rhoErde[DIMAXI+1];
  double cpErde[DIMAXI+1];
  MatrixQ Q;
  double T0[DIMAXI+1];
  KMatrix B1, B2;
  double *B1_ptr_ptr[DIMAXI+1][DimRad+1];
  double **B1_ptr[DIMAXI+1];
  double *B2_ptr_ptr[DIMAXI+1][DimRad+1];
  double **B2_ptr[DIMAXI+1];
  Matrix Tneu;
  double gpar6;
  double gpar5;
  double gpar4;
  double gpar3;
  double gpar2;
  double gpar1;
  double Sondenlaenge;
  double TMonitor;
  double u_min;} pas_config;
  
void default_config(pas_config* cfg);
double calculateEWS_pas(pas_config *cfg);
double calculateEWS_C(pas_config *cfg);

static void test_calc_substep(void **state)
{
  pas_config cfg_C, cfg_pas;
  default_config(&cfg_C);
  default_config(&cfg_pas);
  double T_source = calculateEWS_C(&cfg_C);
  double T_source_ref = calculateEWS_pas(&cfg_pas);
  assert_double_almost_equal(T_source, T_source_ref);
  assert_array_almost_equal(&cfg_C.TEarth[0][0], &cfg_pas.TEarth[0][0], sizeof(cfg_C.TEarth)/sizeof(double));
  assert_array_almost_equal(&cfg_C.Q0[0], &cfg_pas.Q0[0], sizeof(cfg_C.TEarth)/sizeof(double));
}

static void test_calc_substep_0(void **state)
{
  pas_config cfg_C, cfg_pas;
  default_config(&cfg_C);
  default_config(&cfg_pas);
  cfg_C.Iteration = cfg_pas.Iteration = 0;
  cfg_C.simstep--;
  cfg_pas.simstep--;
  double T_source = calculateEWS_C(&cfg_C);
  double T_source_ref = calculateEWS_pas(&cfg_pas);
  assert_double_almost_equal(T_source, T_source_ref);
  assert_array_almost_equal(&cfg_C.TEarth[0][0], &cfg_pas.TEarth[0][0], sizeof(cfg_C.TEarth)/sizeof(double));
  assert_array_almost_equal(&cfg_C.Q0[0], &cfg_pas.Q0[0], sizeof(cfg_C.Q0)/sizeof(double));
}

int main(void)
{
  const struct CMUnitTest tests[] = {
    cmocka_unit_test(test_calc_substep),
    cmocka_unit_test(test_calc_substep_0),
    //    cmocka_unit_test(test_),
  };
  return cmocka_run_group_tests(tests, NULL, NULL);
}

double calculateEWS_C(pas_config *cfg)
{
  unsigned int i, j, l;
  unsigned int dim_ax = cfg->DimAxi;
  unsigned int dim_rad = cfg->DimRad_;
  double U_brine = cfg->cpSole * cfg->Massenstrom / cfg->AnzahlSonden;
  double dt = cfg->Zeitschritt * 60;
  double dt_step = dt / cfg->subdt;
  double *L1 = (U_brine > 0.)?cfg->L1run:cfg->L1stop;
  T_soil_parameters pump_parameters = {.T_soil_tensor=T_soil_tensor_new_from_pas((U_brine > 0.)?cfg->B1_ptr:cfg->B2_ptr, dim_ax, dim_rad), .L=&L1[1]};
  T_brine_static_parameters prm_static = T_brine_static_parameters_create(L1, dim_ax, U_brine);
  T_brine_parameters prm = T_brine_parameters_create(L1, dim_ax, (U_brine > 0.)?cfg->substep_run:cfg->substep_stop, U_brine, cfg->mcpSole, dt_step);
  if(cfg->Stationaer)
    {
      pump_parameters.T_brine_refresh = (T_brine_refresh_fun)&T_brine_static;
      pump_parameters.T_brine_parameters = &prm_static;
    }
  else
    {
      pump_parameters.T_brine_refresh = (T_brine_refresh_fun)&T_brine;
      pump_parameters.T_brine_parameters = &prm;
    }
  int simstepn = (cfg->simstep + cfg->numrows * (cfg->Jahr - 1)) % (10080 / cfg->Zeitschritt * cfg->RepRandbed);
  if(simstepn == 0)
    simstepn = 10080 / cfg->RepRandbed / cfg->Zeitschritt;
  unsigned int n_Q0 = (simstepn - 1) * cfg->subdt;
  double *T_soil = malloc((DimRad+2)*dim_ax*sizeof(double));
  l = 0;
  for(j=0; j<dim_rad+2; j++)
    for(i=1; i<=dim_ax; i++)
      T_soil[l++] = cfg->TEarth[i][j];
  double *sum_Q0 = malloc(dim_ax*sizeof(double));
  for(i=0; i<dim_ax; i++)
    sum_Q0[i] = cfg->Q0[i+1] * n_Q0;
  double *Q_wall = malloc(dim_ax*sizeof(double));
  for(i=0; i<dim_ax; i++)
    Q_wall[i] = 0.;
  double *T_U = T_U_from_pas(cfg->TDown, cfg->TUp, (unsigned int)dim_ax);
  unsigned int n_steps = cfg->subdt;
  double T_source;
  if(cfg->Iteration == 0 && ((cfg->simstep+cfg->numrows*(cfg->Jahr-1))*cfg->Zeitschritt) % (60*24*7*cfg->RepRandbed)  ==  0)
    {
      double *T_soil_tensor = T_soil_tensor_new(dim_ax, dim_rad);
      for(i=0; i<dim_rad*(dim_rad+2)*dim_ax; i++)
	T_soil_tensor[i] = pump_parameters.T_soil_tensor[i];
      T_source = (n_steps-1)*soil_step(T_soil, cfg->TSink, sum_Q0,
				       dim_ax, dim_rad,
				       n_steps-1,
				       Q_wall,
				       T_U,
				       &pump_parameters);
      n_Q0 += n_steps-1;
      T_soil_tensor_fill_id(dim_ax, dim_rad, pump_parameters.T_soil_tensor);
      T_source += soil_step(T_soil, cfg->TSink, sum_Q0,
			    dim_ax, dim_rad,
			    1,
			    Q_wall,
			    T_U,
			    &pump_parameters);
      n_Q0++;
      T_source /= n_steps;
      int Woche;
      if (! cfg->Starttemp)
	Woche = (cfg->simstep+cfg->numrows*(cfg->Jahr-1)-1) / (10080 / cfg->Zeitschritt * cfg->RepRandbed) + 1;
      else
	Woche = (cfg->simstep-1) / (10080 / cfg->Zeitschritt * cfg->RepRandbed) + 1;
      unsigned int dim_t = Woche+1;
      double *T_soil_boundary = malloc(dim_ax*sizeof(double));
      double *d_lambda_soil = malloc(dim_ax*sizeof(double));
      double *g = malloc(dim_t*dim_ax*sizeof(double));
      double *t = t_range(dim_t, cfg->RepRandbed * 604800, 1);
      double *c_V_soil = malloc(dim_ax*sizeof(double));
      for(i=0; i<dim_ax; i++)
	c_V_soil[i] = cfg->cpErde[i+1] * cfg->rhoErde[i+1];

      if(cfg->gfunction)
	{
	  g_func_parameters prm = {.g_coefs={cfg->gpar1, cfg->gpar2, cfg->gpar3, cfg->gpar4, cfg->gpar5, cfg->gpar6}, .u_min=cfg->u_min, .L=cfg->Sondenlaenge, .go_const=default_go_const};
	  g_func(t, dim_t,
		 c_V_soil,
		 &cfg->lambdaErde[1],
		 dim_ax,
		 &cfg->Rechenradius,
		 1,
		 g,
		 &prm);
	}
      else
	  g_cone(t, dim_t,
		 c_V_soil,
		 &cfg->lambdaErde[1],
		 dim_ax,
		 &cfg->Rechenradius,
		 1,
		 g,
		 NULL);
      double *q = malloc(dim_t*dim_ax*sizeof(double));
      
      for(j=0; j<dim_ax; j++)
	{
	  d_lambda_soil[j] = cfg->lambdaErde[j+1] * cfg->Sondenlaenge / dim_ax;
	  cfg->Q[j+1][Woche] = sum_Q0[j] / n_Q0;
	  T_soil_boundary[j] = cfg->T0[j+1];
	}
      l = 0;
      for(i=0; i<dim_t; i++)
	for(j=0; j<dim_ax; j++)
	  q[l++] = cfg->Q[j+1][i];

      Delta_T_boundary_1(g,
			 Woche, dim_ax,
			 q,
			 d_lambda_soil, T_soil_boundary);
      for(j=0; j<dim_ax; j++)
	T_soil[(dim_rad+1)*dim_ax + j] = T_soil_boundary[j];
      T_soil_refresh(T_soil, T_soil_tensor, dim_ax, dim_rad);
      free(d_lambda_soil);
      free(T_soil_tensor);
      free(T_soil_boundary);
      free(g);
      free(q);
      free(t);
      free(c_V_soil);
    }
  else
    {
      T_source = soil_step(T_soil, cfg->TSink, sum_Q0,
			   dim_ax, dim_rad,
			   n_steps,
			   Q_wall,
			   T_U,
			   &pump_parameters);
      n_Q0 += n_steps;
    }
  l = 0;
  for(j=0; j<dim_rad+2; j++)
    for(i=1; i<=dim_ax; i++)
      cfg->TEarth[i][j] = T_soil[l++];
  for(i=0; i<dim_ax; i++)
    cfg->Q0[i+1] = sum_Q0[i]/n_Q0;
  free(T_soil);
  free(sum_Q0);
  free(T_U);
  free(Q_wall);
  free(pump_parameters.T_soil_tensor);
  T_brine_static_parameters_free(&prm_static);
  T_brine_parameters_free(&prm);
  return T_source;
}

double *T_U_from_pas(double *TDown, double *TUp, unsigned int dim_ax)
{
  unsigned int i;
  double *T_U = malloc(2*dim_ax*sizeof(double));
  for(i=0; i<dim_ax; i++)
    {
      T_U[i] = TDown[1+i];
      T_U[DIMAXI+i] = TUp[1+i];
    }
  return T_U;
}

T_brine_static_parameters T_brine_static_parameters_create(double *L_pas, unsigned int dim_ax, double L0)
{
  unsigned int i;
  T_brine_static_parameters prm = {.kappa_brine=malloc(dim_ax*sizeof(double)), .kappa_soil=malloc(dim_ax*sizeof(double)), .L=malloc(dim_ax*sizeof(double))};
  for(i=0; i<dim_ax; i++)
    {
      prm.L[i] = L_pas[1+i];
      prm.kappa_brine[i] = L0 / (0.5 * prm.L[i] + L0);
      prm.kappa_soil[i] = prm.L[i] / (prm.L[i] + 2*L0);
    }
  return prm;
}
void T_brine_static_parameters_free(T_brine_static_parameters* prm)
{
  free(prm->L);
  free(prm->kappa_brine);
  free(prm->kappa_soil);
}
T_brine_parameters T_brine_parameters_create(double *L_pas, unsigned int dim_ax, unsigned int substep, double L0, double mcpSole, double dt)
{
  unsigned int i;
  T_brine_parameters prm = {.n_sub_steps=substep, .kappa_ax=L0 / mcpSole * dt / substep, .kappa_rad=malloc(dim_ax*sizeof(double)), .lambda_brine=malloc(dim_ax*sizeof(double))};
  for(i=0; i<dim_ax; i++)
    {
      prm.kappa_rad[i] = 0.5 * L_pas[i+1] / substep * dt / mcpSole;
      prm.lambda_brine[i] = 0.5 * L_pas[i+1] / substep;
    }
  return prm;
}
void T_brine_parameters_free(T_brine_parameters* prm)
{
  free(prm->kappa_rad);
  free(prm->lambda_brine);
}
double *T_soil_tensor_new(unsigned int dim_ax, unsigned int dim_rad)
{
  double *T = malloc(dim_rad*(dim_rad+2)*dim_ax*sizeof(double));
  return T;
}

double *T_soil_tensor_new_from_pas(double ***B, unsigned int dim_ax, unsigned int dim_rad)
{
  double *T = T_soil_tensor_new(dim_ax, dim_rad);
  T_soil_tensor_fill(B, dim_ax, dim_rad, T);
  return T;
}

double TBRINE(Matrix T,
	      double *TDown,
	      double *TUp,
	      double TSink,
	      double L0,
	      double *L, double *La,
	      int Zeitschritt, int subdt, int substep,
	      double *QWand,
	      double mcpSole, double mcpSoleUp, double mcpSoleDown,
	      int DimAxi,
	      _Bool stationaer,
	      _Bool KoaxialSonde
	      )
{
  unsigned int i;
  double *T_soil = malloc(DimAxi*sizeof(double));
  double *T_U = T_U_from_pas(TDown, TUp, (unsigned int)DimAxi);
  double T_out;
  double dt = Zeitschritt * 60. / subdt;

  for(i=0; i<(unsigned int)DimAxi; i++)
    T_soil[i] = T[i+1][1];
  if(stationaer)
    {
      T_brine_static_parameters prm = T_brine_static_parameters_create(L, DimAxi, L0);
      T_out = T_brine_static(T_soil, T_U, &QWand[1],
		      DimAxi,
		      TSink,
		      &prm);
      T_brine_static_parameters_free(&prm);
    }
  else
    {
      T_brine_parameters prm = T_brine_parameters_create(L, DimAxi, substep, L0, mcpSole, dt);
      T_out = T_brine(T_soil, T_U, &QWand[1],
		      DimAxi,
		      TSink,
		      &prm);
      T_brine_parameters_free(&prm);
    }
  for(i=1; i<=(unsigned int)DimAxi; i++)
    {
      QWand[i] *= dt;
      TDown[i] = T_U[i-1];
      TUp[i] = T_U[DIMAXI+i-1];
    }
  free(T_soil);
  free(T_U);
  return T_out;
}

double* t_range(unsigned int dim_t, double dt, unsigned int i0)
{
  unsigned int i;
  double *t = malloc(dim_t*sizeof(double));
  for(i=0; i<dim_t; i++) t[i] = dt * (i0+i);
  return t;
}

double RandAussen_gfunc(
			int k, int Woche,
			int Zeitschritt, long simstep,
			int RepRandbed,
			MatrixQ Q,
			double cpErd,
			double rhoErd,
			double lambdaErd,
			double Rechenradius, double Sondenlaenge,
			double gpar1, double gpar2,double gpar3,double gpar4,
			double gpar5,double gpar6,
			int DimAxi,
			double u_min)
// Replacement for original code for tests
{
  unsigned int i;
  unsigned int dim_t = Woche + 1;
  double *t = t_range(dim_t, RepRandbed * 604800, 1);
  double *g = malloc(dim_t*sizeof(double));
  double c_V_soil = cpErd * rhoErd;
  double T_out = 0.;
  double *q = malloc(dim_t*sizeof(double));
  for(i=0; i<dim_t; i++) q[i] = Q[k][i];
  g_func_parameters prm = {
    .g_coefs={gpar1, gpar2, gpar3, gpar4, gpar5, gpar6}, .u_min=u_min, .L=Sondenlaenge,
    .go_const=default_go_const};
  g_func(t, dim_t, &c_V_soil, &lambdaErd, 1, &Rechenradius, 1, g, &prm);
  lambdaErd *= Sondenlaenge / DimAxi;
  Delta_T_boundary_1(g, dim_t-1, 1, q, &lambdaErd, &T_out);
  free(t);
  free(g);
  free(q);
  return T_out;
}

double RandAussen(int k, int Woche,
		  int Zeitschritt, long simstep,
		  int RepRandbed,
		  MatrixQ Q,
		  double cpErd,double rhoErd,double lambdaErd,
		  double Rechenradius,double Sondenlaenge,
		  int DimAxi)
{
  unsigned int i;
  unsigned int dim_t = Woche + 1;
  double *t = malloc(dim_t*sizeof(double));
  for(i=0; i<dim_t; i++) t[i] = RepRandbed * 604800 * i;
  double *g = malloc(dim_t*sizeof(double));
  double c_V_soil = cpErd * rhoErd;
  double *q = malloc(dim_t*sizeof(double));
  double T_out = 0.;
  for(i=0; i<dim_t; i++) q[i] = Q[k][i];
  g_cone(t, dim_t, &c_V_soil, &lambdaErd, 1, &Rechenradius, 1, g, NULL);
  lambdaErd *= Sondenlaenge / DimAxi;
  Delta_T_boundary_1(g, dim_t-1, 1, q, &lambdaErd, &T_out);
  free(t);
  free(g);
  free(q);
  return T_out;
}

void WriteStep(int filestep, double Massenstrom, double TSink, double QSource,
	       double TSource,
	       double TEarth,
	       double p, _Bool laminar)
{}
void ReadStep(int filestep, double Massenstrom, double TSink, double QSource)
{}

void default_config(pas_config *cfg)
{
  unsigned int i, j;
  double u_min = -4.0;
  int Woche = DimT-1;

  double mcpSole = 144014.53;  // kJ/K
  int subdt = 97;
  double L1run = 905.79;
  double L1stop = 1507.91;
  double x = Def_cpSole * Def_Massenstrom / Def_AnzahlSonden;
  if(x < L1run) x = L1run;
  double Lm_min = mcpSole / x;
  double dt = Def_Zeitschritt * 60;
  double dt_step = dt / subdt;
  int substep_run = (int)(Def_Sicherheit1 * dt_step / Lm_min) + 1;
  int substep_stop = (int)(Def_Sicherheit1 * dt_step / mcpSole * L1stop) + 1;

  pas_config _cfg = {.Iteration =1, .DimAxi =DIMAXI, .DimRad_ =DimRad,
		     .MonitorAxi =0, .MonitorRad =0,
		     .TEarth = {{ NAN },
			       { 10.3, 10.3, 10.3, 10.3, 10.3, 10.3, 10.3},
			       { 11.3, 11.3, 11.3, 11.3, 11.3, 11.3, 11.3},
			       { 12.3, 12.3, 12.3, 12.3, 12.3, 12.3, 12.3}},
		     .TUp = { 0. },
		     .TUpOld = { 0. },
		     .TDownOld = { 0. },
		     .TDown = { 0. },
		     .Q0Old = { 0. },
		     .Q0 = { 0. },
		     .TSourceOld = 0.,
		     .TSource = 0.,
		     .TSourceMin =0.,
		     .TSourceMax =0.,
		     .TSink =9.,
		     .TSinkMin =0.,
		     .TSinkMax =0.,
		     .QSource =Def_QSource,
		     .Massenstrom =Def_Massenstrom,
		     .cpSole =Def_cpSole,
		     .p = NAN,
		     .laminar = false,
		     .readFile = false,
		     .simstep =1 + (Woche - 1) * 10080 / Def_Zeitschritt * Def_RepRandbed,
		     .StepWrite = 1,
		     .einschwingen = false,
		     .Allsteps = false,
		     .writeFile = false,
		     .Leistung = false,
		     .gfunction = true,
		     .RepRandbed = Def_RepRandbed,
		     .Zeitschritt = Def_Zeitschritt,
		     .Jahr = 1,
		     .numrows = Def_Simulationsdauer * 60 % Def_Zeitschritt,
		     .Starttemp = false,
		     .DeltaT =Def_DeltaT,
		     .subdt =subdt,
		     .AnzahlSonden =Def_AnzahlSonden,
		     .Rechenradius =Def_Rechenradius,
		     .Stationaer = false,
		     .mcpSole = mcpSole,
		     .substep_run =substep_run,
		     .L1run = {0., 905.79, 905.79, 905.79},
		     .substep_stop =substep_stop,
		     .L1stop = {0., 1507.91, 1507.91, 1507.91},
		     .lambdaErde = {NAN, Def_lambdaErde, Def_lambdaErde + 0.1, Def_lambdaErde - 0.1},
		     .rhoErde = {NAN, 2600., 2500., 2600.},
		     .cpErde = {NAN, 1000., 1010., 990.},
		     .Q = {{ 0. }},
		     .B1 = {{{1.0,  0.0,  0.0,  0.0, 0.0,  0.0,  0.0},
			     { 0.0 },
			     { 0.0 },
			     { 0.0 },
			     { 0.0 },
			     { 0.0 }},
			    {{1.0,  0.0,  0.0,  0.0, 0.0,  0.0,  0.0},
			     {3.33224144e-02,  9.58687328e-01,  7.97682872e-03,  1.34237716e-05,  5.26854727e-09,  5.04601074e-13,  3.49782250e-17},
			     {2.42895507e-05,  1.42773673e-03,  9.95189061e-01,  3.35759525e-03 ,  1.31778533e-06,  1.26212381e-10,  8.74886177e-15},
			     {8.64494708e-09,  5.08148902e-07,  7.10112100e-04,  9.98504925e-01,  7.84371038e-04,  7.51240234e-08,  5.20748989e-12},
			    {7.90680723e-13,  4.64761134e-11,  6.49479914e-08,  1.82786465e-04,  9.99625619e-01,  1.91516405e-04,  1.32756434e-08},
			    {1.81618290e-17,  1.06755002e-15,  1.49184655e-12,  4.19858032e-09,  4.59311293e-05,  9.99815440e-01,  1.38624347e-04}},
			   {{1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0},
			    {3.33200695e-02,  9.58549492e-01,  8.11566439e-03,  1.47674772e-05,  6.25334385e-09,  6.46170487e-13,  4.84846977e-17},
			    {2.54499880e-05,  1.49594709e-03,  9.94847189e-01,  3.62987661e-03,  1.53708493e-06,  1.58830050e-10,  1.19176396e-14},
			    {9.77239210e-09,  5.74419978e-07,  7.65989709e-04,  9.98387114e-01,  8.46224553e-04,  8.74420702e-08,  6.56112036e-12},
			    {9.64304301e-13,  5.66816855e-11,  7.55850936e-08,  1.97193611e-04,  9.99596093e-01,  2.06622251e-04,  1.55036752e-08},
			    {2.39760264e-17,  1.40930782e-15,  1.87931361e-12,  4.90293285e-09,  4.97170537e-05,  9.99800225e-01,  1.50052829e-04}},
			   {{1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0},
			    {3.33249178e-02,  9.58834477e-01,  7.82797122e-03,  1.26294002e-05,  4.74533384e-09,  4.35656603e-13,  2.89996267e-17},
			    {2.40541595e-05,  1.41390047e-03,  9.95341615e-01,  3.21922081e-03,  1.20958060e-06,  1.11048409e-10,  7.39197430e-15},
			    {8.19617559e-09,  4.81770170e-07,  6.79889491e-04,  9.98568615e-01, 7.50936317e-04,  6.89414857e-08,  4.58911293e-12},
			    {7.18574968e-13,  4.22377462e-11,  5.96072600e-08,  1.75218474e-04,  9.99641128e-01,  1.83581786e-04,  1.22201827e-08},
			    {1.58500493e-17,  9.31663905e-16,  1.31479394e-12,  3.86490147e-09,  4.41073123e-05,  9.99822770e-01,  1.33118868e-04}}},
		    .B2 = {{{1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0},
			    { 0.0 },
			    { 0.0 },
			    { 0.0 },
			    { 0.0 },
			    { 0.0 }},
			   {{1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0},
			    {5.48656829e-02,  9.37231586e-01,  7.88944939e-03,  1.32767257e-05,  5.21083485e-09,  4.99073601e-13,  3.45950685e-17},
			    {3.99929840e-05,  1.41209710e-03,  9.95188997e-01,  3.35759515e-03,  1.31778529e-06,  1.26212377e-10,  8.74886150e-15},
			    {1.42339903e-08,  5.02582566e-07,  7.10112077e-04,  9.98504925e-01,  7.84371038e-04,  7.51240234e-08,  5.20748989e-12},
			    {1.30186358e-12,  4.59670074e-11,  6.49479893e-08,  1.82786465e-04, 9.99625619e-01,  1.91516405e-04,  1.32756434e-08},
			    {2.99036300e-17,  1.05585593e-15,  1.49184651e-12,  4.19858032e-09,  4.59311293e-05,  9.99815440e-01,  1.38624347e-04}},
			   {{1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0},
			    {5.48618642e-02,  9.37096753e-01,  8.02677042e-03,  1.46057234e-05,  6.18484859e-09,  6.39092735e-13,  4.79536264e-17},
			    {4.19036877e-05,  1.47956141e-03,  9.94847121e-01,  3.62987648e-03,  1.53708487e-06,  1.58830044e-10,  1.19176392e-14},
			    {1.60903520e-08,  5.68128137e-07,  7.65989683e-04,  9.98387114e-01,  8.46224553e-04,  8.74420702e-08,  6.56112036e-12},
			    {1.58773773e-12,  5.60608294e-11,  7.55850910e-08,  1.97193611e-04,  9.99596093e-01,  2.06622251e-04,  1.55036752e-08},
			    {3.94767936e-17,  1.39387113e-15,  1.87931355e-12,  4.90293285e-09,  4.97170537e-05,  9.99800225e-01,  1.50052829e-04}},
			   {{1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0},
			    {5.48697596e-02,  9.37375529e-01,  7.74221612e-03,  1.24910457e-05,  4.69334891e-09,  4.30884004e-13,  2.86819371e-17},
			    {3.96053774e-05,  1.39841125e-03,  9.95341553e-01,  3.21922071e-03,  1.20958056e-06,  1.11048406e-10,  7.39197407e-15},
			    {1.34950726e-08,  4.76492398e-07,  6.79889470e-04,  9.98568615e-01,  7.50936317e-04,  6.89414857e-08,  4.58911293e-12},
			    {1.18313977e-12,  4.17750335e-11,  5.96072581e-08,  1.75218474e-04, 9.99641128e-01,  1.83581786e-04,  1.22201827e-08},
			    {2.60972405e-17,  9.21457567e-16,  1.31479389e-12,  3.86490147e-09, 4.41073123e-05,  9.99822770e-01,  1.33118868e-04}}},
		    .Tneu = {{ 0. }},
		    .Sondenlaenge =Def_Sondenlaenge,
		    .TMonitor = NAN,
		    .u_min = u_min};
  *cfg = _cfg;
  for(i=1; i<=DIMAXI; i++)
    cfg->T0[i] = cfg->TEarth[i][DimRad];
  for(i=1; i<=DIMAXI; i++)
    for(j=1; j<=DimRad+1; j++)
      cfg->TEarthOld[i][j] = cfg->TEarth[i][j];
  for(i=0; i<=DIMAXI; i++)
    {
      cfg->B1_ptr[i] = &cfg->B1_ptr_ptr[i][0];
      cfg->B2_ptr[i] = &cfg->B2_ptr_ptr[i][0];
      for(j=0; j<=DimRad; j++)
	{
	  cfg->B1_ptr_ptr[i][j] = &cfg->B1[i][j][0];
	  cfg->B2_ptr_ptr[i][j] = &cfg->B2[i][j][0];
	}
    }
}
double calculateEWS_pas(pas_config *cfg)
{
  return calculateEWS(cfg->Iteration, cfg->DimAxi, cfg->DimRad_,
		      cfg->MonitorAxi,
		      cfg->MonitorRad,
		      cfg->TEarthOld,
		      cfg->TEarth,
		      cfg->TUp,
		      cfg->TUpOld,
		      cfg->TDownOld,
		      cfg->TDown,
		      cfg->Q0Old,
		      cfg->Q0,
		      cfg->TSourceOld,
		      cfg->TSource,
		      cfg->TSourceMin,
		      cfg->TSourceMax,
		      cfg->TSink,
		      cfg->TSinkMin,
		      cfg->TSinkMax,
		      cfg->QSource,
		      cfg->Massenstrom,
		      cfg->cpSole,
		      cfg->p,
		      cfg->laminar,
		      cfg->readFile,
		      cfg->simstep,
		      cfg->StepWrite,
		      cfg->einschwingen,
		      cfg->Allsteps,
		      cfg->writeFile,
		      cfg->Leistung,
		      cfg->gfunction,
		      cfg->RepRandbed,
		      cfg->Zeitschritt,
		      cfg->Jahr,
		      cfg->numrows,
		      cfg->Starttemp, 
		      cfg->DeltaT,
		      cfg->subdt,
		      cfg->AnzahlSonden,
		      cfg->Rechenradius,
		      cfg->Stationaer,
		      cfg->mcpSole,
		      cfg->substep_run,
		      cfg->L1run,
		      cfg->substep_stop,
		      cfg->L1stop,
		      cfg->lambdaErde,
		      cfg->rhoErde,
		      cfg->cpErde,
		      cfg->Q,
		      cfg->T0,
		      cfg->B1,
		      cfg->B2,
		      cfg->Tneu,
		      cfg->gpar6,
		      cfg->gpar5,
		      cfg->gpar4,
		      cfg->gpar3,
		      cfg->gpar2,
		      cfg->gpar1,
		      cfg->Sondenlaenge,
		      cfg->TMonitor,
		      cfg->u_min);
}
