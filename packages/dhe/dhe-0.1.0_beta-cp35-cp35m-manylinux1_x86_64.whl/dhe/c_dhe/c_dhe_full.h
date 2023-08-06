#ifndef __DHE_FULL_H__
#define __DHE_FULL_H__

typedef struct {
  double *T_sink;
  double *T_source;
  double *T_soil;
} CalcPOutput;

typedef struct {
    /// Values of g function at ln(t/ts) = (-4, -2, 0, 2, 3)
  double g_coefs[5]; // default: [4.82, 5.69, 6.29, 6.57, 6.60]
    /// Distance of DHE's [m]
  double d_DHE; // default=10.,
} TSoil0Parameters;

/// Material properties
typedef struct {
  double rho; // default=1180.
  double c; // default=3040.
  double lambda; // default=0.81
} MaterialProperties;

/// Soil layer properties
typedef struct {
  double rho;    // default=2600.
  double c;      // default=1000.
  double lambda; // default=2.0
  double d;      // Thickness of layer [m] possibly infinity
} SoilLayerProperties;
/// Fluid properties
typedef struct {
  double rho; // default=1050.
  double c; //default=3875.
  double lambda; //default=0.449
  double nu; //default=0.415E-5
} FluidProperties;

typedef struct {
    /// x coordinate of the DHE [m]
  double x; // default=0.
    /// y coordinate of the DHE [m]
  double y; // default=0.
    /// Length of DHE [m]
  double L; // default=100.
    /// Diameter of DHE [m]
  double D; // default=0.026
    /// Diameter of bore hole [m]
  double D_borehole; // default=0.115
    /// Thickness of DHE pipe [m]
  double thickness; // default=0.
    /// Thermal pipe resistance [Km/W]
  double Ra; // default=0.
    /// Borehole thermal resistance [Km/W]
  double Rb; // default=0.1
    /// Thermal resistance [Km/W]
  double R1; // default=0.0
  MaterialProperties fill_properties;
  FluidProperties brine_properties;
    /// Mass throughput per DHE if pump is on [kg/s]
  double Phi_m; // default=0.4
  TSoil0Parameters T_soil_0_parameters;
} DHE2 ;


typedef struct {
    /// Mean temperature of soil [°C]
  double T_soil_mean; // default=9.8
    /// Axial gradient of temperature of soil [K/m]
  double T_grad; // default=0.03
} SoilParameters;

typedef double* g_func(void *self,
		       double *t,
		       unsigned int dim_t,
		       double *c_V_soil,
		       double *lambda_soil,
		       unsigned int dim_ax,
		       unsigned int dim_rad,
		       double *r
		       );

typedef double TBrineMethod(void* self,
			    double *T_soil,
			    double *T_U,
			    double *Q_wall,
			    unsigned int dim_ax,
			    double T_sink);
TBrineMethod T_brine_stationary, T_brine_dynamic;

typedef struct {
  g_func *method;
  void *data;
} GMethod;

typedef struct {
    /// Number of sampling points in axial direction
  unsigned int dim_ax; // default: 4
    /// Number of sampling points in radial direction
  unsigned int dim_rad; // default=5,
  TBrineMethod* T_brine_method;
  /// Method for computing g function
  GMethod g_method;

  /// Soil layers
  SoilLayerProperties *soil_layers;
  unsigned int n_soil_layers;

  /// Radius of calculation [m]
  double R; // default=1.5
    /// Multiplier for the n_steps variable
  double optimal_n_steps_multiplier; // default=2.
    /// Grid parameter for radial partition of domain of calculation
  double Gamma; // default=2.0
    /// Fraction of adiabatic boundary contitions
  double adiabat; // default=0.0
    /// Factor for n_steps [m]
  unsigned int n_steps_0; // default=4
    /// Duration between two boundary condition refreshes [s]
  double dt_boundary_refresh; // default=7 * 24 * 3600.
    /// Sampling step [s]
  double dt; // default=3600.
  /// [s]
  double t0; // default=0.
  SoilParameters soil_parameters;
} GlobalParameters;

void free_global_parameters(GlobalParameters *env);

typedef struct {
  double g_coefs[6];
  double u_min;
  double L;
  double go_const;
} GFuncParameters;
typedef struct {} GConeParameters;

void calc_P_2(double *t, double *P, unsigned int dim_t, DHE2 *dhe, unsigned int n_DHE, GlobalParameters *env, double precision, CalcPOutput *out);


#endif // __DHE_FULL_H__
