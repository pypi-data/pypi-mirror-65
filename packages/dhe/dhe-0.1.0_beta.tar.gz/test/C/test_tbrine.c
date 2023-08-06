#define UNIT_TESTING
#include <stdarg.h>
#include <stddef.h>
#include <setjmp.h>
#include <string.h>
#include <stdlib.h>
#include <math.h>
#include <cmocka.h>
#include "cmocka_utils.h"

#include "original/tbrine.c"
#include <c_dhe/c_dhe.c>

#define DimAxi 3
#define SizeAxi (DimAxi + 1)

typedef struct {
  Matrix T;
  double TDown[SizeAxi];
  double TUp[SizeAxi];
  double TSink;
  double L0;
  double L[SizeAxi];
  double La[SizeAxi];
  int Zeitschritt;
  int subdt, substep;
  double mcpSole, mcpSoleUp, mcpSoleDown;
  _Bool stationaer, Koaxialsonde;
} config;

typedef struct {
  double T_soil[DimAxi];
  double T_U[2*DimAxi];
  double dt;
  double dC_brine;
  double U_brine;
  double L[DimAxi];
  double T_sink;
  double kappa_rad[DimAxi];
  double lambda_brine[DimAxi];
  double kappa_brine[DimAxi];
  double kappa_soil[DimAxi];
  T_brine_static_parameters static_parameters;
  T_brine_parameters parameters;
} c_config;

void pas2c(config *pas_c, c_config *cfg_c)
{
  unsigned int i;
  double U_brine = pas_c->L0;
  double dt = pas_c->Zeitschritt * 60. / pas_c->subdt;
  double kappa_ax = U_brine / pas_c->mcpSole * dt / pas_c->substep;
  c_config c = {
    .dt = dt,
    .dC_brine = pas_c->mcpSole,
    .U_brine = U_brine,
    .T_sink = pas_c->TSink,
    .parameters = {.n_sub_steps = pas_c->substep,
		   .kappa_ax = kappa_ax}
  };
  for(i=0; i<DimAxi; i++)
    {
      c.T_soil[i] = pas_c->T[1+i][1];
      c.L[i] = pas_c->L[1+i];
      c.T_U[i] = pas_c->TDown[1+i];
      c.T_U[DimAxi+i] = pas_c->TUp[1+i];
      c.kappa_brine[i] = U_brine / (0.5 * c.L[i] + U_brine);
      c.kappa_soil[i] = c.L[i] / (c.L[i] + 2*U_brine);
      c.kappa_rad[i] = 0.5 * c.L[i] / c.parameters.n_sub_steps * dt / c.dC_brine;
      c.lambda_brine[i] = 0.5 * c.L[i] / c.parameters.n_sub_steps;
    }
  *cfg_c = c;
  cfg_c->static_parameters.kappa_brine = cfg_c->kappa_brine;
  cfg_c->static_parameters.kappa_soil = cfg_c->kappa_soil;
  cfg_c->static_parameters.L = cfg_c->L;
  cfg_c->parameters.kappa_rad = cfg_c->kappa_rad;
  cfg_c->parameters.lambda_brine = cfg_c->lambda_brine;
}

config configs[] = {
  {
    .T = {{NAN, NAN}, {NAN, 2.}, {NAN, 3.}, {NAN, 4.}},
    .TDown = {0., 0., 0., 0.},
    .TUp = {0., 0., 0., 0.},
    .TSink = 30.,
    .L0 = 0.001,
    .L = {NAN, 0.001, 0.03, 0.02},
    .La = {0.001, 0.002, 0.003, 0.002},
    .Zeitschritt = 3,
    .subdt = 1,
    .substep = 5,
    .mcpSole = 0.37,
    .mcpSoleUp = 0.65,
    .mcpSoleDown = 0.8,
    .stationaer = 0,
    .Koaxialsonde = 0
  },
  {
    .T = {{NAN, NAN}, {NAN, 2.}, {NAN, 3.}, {NAN, 4.}},
    .TDown = {NAN, 4.17812774, 2.33856008, 1.8860926},
    .TUp = {NAN, 1.76708029, 1.6359369, 1.4983018},
    .TSink = 30.,
    .L0 = 0.001,
    .L = {NAN, 0.001, 0.03, 0.02},
    .La = {0.001, 0.002, 0.003, 0.002},
    .Zeitschritt = 3,
    .subdt = 1,
    .substep = 5,
    .mcpSole = 0.37,
    .mcpSoleUp = 0.65,
    .mcpSoleDown = 0.8,
    .stationaer = 0,
    .Koaxialsonde = 0
  },
  {
    .T = {{NAN, NAN}, {NAN, 2.}, {NAN, 3.}, {NAN, 4.}},
    .TDown = {0., 0., 0., 0.},
    .TUp = {0., 0., 0., 0.},
    .TSink = 0.,
    .L0 = 0.001,
    .L = {NAN, 0.001, 0.03, 0.02},
    .La = {0.001, 0.002, 0.003, 0.002},
    .Zeitschritt = 1,
    .subdt = 1,
    .substep = 1,
    .mcpSole = 0.37,
    .mcpSoleUp = 0.65,
    .mcpSoleDown = 0.8,
    .stationaer = 0,
    .Koaxialsonde = 0
  },
  {
    .T = {{NAN, NAN}, {NAN, 0.}, {NAN, 0.}, {NAN, 0.}},
    .TDown = {NAN, 4.17812774, 2.33856008, 1.8860926},
    .TUp = {NAN, 1.76708029, 1.6359369, 1.4983018},
    .TSink = 0.,
    .L0 = 0.001,
    .L = {NAN, 0.001, 0.03, 0.02},
    .La = {0.001, 0.002, 0.003, 0.002},
    .Zeitschritt = 1,
    .subdt = 1,
    .substep = 1,
    .mcpSole = 0.37,
    .mcpSoleUp = 0.65,
    .mcpSoleDown = 0.8,
    .stationaer = 0,
    .Koaxialsonde = 0
  }
};


static void test_tbrine_U_static(void **state)
{
  unsigned int i;
  for(i=0; i<sizeof(configs)/sizeof(config); i++)
    {
      config cfg = configs[i];
      cfg.substep = 1;
      cfg.stationaer = 1;
      double QWand[SizeAxi] = {0., 0., 0., 0.};
      c_config cfg_c;
      pas2c(&cfg, &cfg_c);
      double T_out_ref = TBRINE(cfg.T,
			 cfg.TDown,
			 cfg.TUp,
			 cfg.TSink,
			 cfg.L0,
			 cfg.L, cfg.La,
			 cfg.Zeitschritt, cfg.subdt, cfg.substep,
			 QWand,
			 cfg.mcpSole, cfg.mcpSoleUp, cfg.mcpSoleDown,
			 DimAxi,
			 cfg.stationaer,
			 cfg.Koaxialsonde);
      double Q_wall[DimAxi] = {0., 0., 0.};
      double T_out = T_brine_static(cfg_c.T_soil,
				    cfg_c.T_U,
				    Q_wall,
				    DimAxi,
				    cfg_c.T_sink,
				    &cfg_c.static_parameters);
      assert_double_almost_equal(T_out, T_out_ref);
      assert_array_almost_equal(&cfg.TDown[1], cfg_c.T_U, DimAxi);
      assert_array_almost_equal(&cfg.TUp[1], &cfg_c.T_U[DimAxi], DimAxi);
      assert_array_almost_equal_factor(&QWand[1], Q_wall, cfg_c.dt, DimAxi);
    }
}

static void test_tbrine_U(void **state)
{
  unsigned int i;
  for(i=0; i<sizeof(configs)/sizeof(config); i++)
    {
      config cfg = configs[i];
      double QWand[SizeAxi] = {0., 0., 0., 0.};
      c_config cfg_c;
      pas2c(&cfg, &cfg_c);
      double T_out_ref = TBRINE(cfg.T,
			 cfg.TDown,
			 cfg.TUp,
			 cfg.TSink,
			 cfg.L0,
			 cfg.L, cfg.La,
			 cfg.Zeitschritt, cfg.subdt, cfg.substep,
			 QWand,
			 cfg.mcpSole, cfg.mcpSoleUp, cfg.mcpSoleDown,
			 DimAxi,
			 cfg.stationaer,
			 cfg.Koaxialsonde);
      double Q_wall[DimAxi] = {0., 0., 0.};
      double T_out = T_brine(cfg_c.T_soil,
			     cfg_c.T_U,
			     Q_wall,
			     DimAxi,
			     cfg_c.T_sink,
			     &cfg_c.parameters);
      assert_double_almost_equal(T_out, T_out_ref);
      assert_array_almost_equal(&cfg.TDown[1], cfg_c.T_U, DimAxi);
      assert_array_almost_equal(&cfg.TUp[1], &cfg_c.T_U[DimAxi], DimAxi);
      assert_array_almost_equal_factor(&QWand[1], Q_wall, cfg_c.dt, DimAxi);
    }
}



int main(void)
{
  const struct CMUnitTest tests[] = {
    cmocka_unit_test(test_tbrine_U_static),
    cmocka_unit_test(test_tbrine_U),
    //    cmocka_unit_test(test_),
  };
  return cmocka_run_group_tests(tests, NULL, NULL);
}
