#include <math.h>
#include "pascal_defs.h"
#include "rand.h"

static double hoch(double a, long b);
static __inline__ double sqr(double x) {  return x*x; }
static long Fakultaet(int x);

//  Quellcode für die Berechnung der aeusseren Randbedingungen 
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
{
  /* Diese Funktion berechnet die Randbedingung mit der g-Function
************************************************************** */
  long double u,STrt,ts,g,go,Rq;
  int i;

  ts = (Sondenlaenge)*(Sondenlaenge) / 9 / lambdaErd * rhoErd * cpErd;
  STrt= 0;
  for(i= 1; i<Woche+1; i++) {
    u = log( i / ts * 604800 *RepRandbed );  // Aenderung 2.10.02 
    if (u>2.5)u=2.5;
    go = 0.5*u + 6.84;
    if (u<u_min)g = go;
    else g = gpar1 + gpar2*u + gpar3*sqr(u) + gpar4*u*sqr(u) +
	   gpar5*sqr(sqr(u)) + gpar6*u*sqr(sqr(u));
    if (u<-2)if ((go-0.3)>g)g=go;
    g = g - log(Rechenradius/Sondenlaenge/0.0005);
    Rq = g / 2 / M_PI / lambdaErd;
    STrt = STrt + (-Q[k][Woche-i+1]+Q[k][Woche-i])/Sondenlaenge*DimAxi*Rq;
  };
  return STrt;
}

double RandAussen(int k, int Woche,
		  int Zeitschritt, long simstep,
		  int RepRandbed,
		  MatrixQ Q,
		  double cpErd,double rhoErd,double lambdaErd,
		  double Rechenradius,double Sondenlaenge,
		  int DimAxi)
{
/* Diese def berechnet die Randbedingung nach der Trichterformel
   von Werner ******************************************************** */
  long double u,u0,W,W_alt,STrt,STrt0;
  int i, j;
  u0=(Rechenradius)*(Rechenradius)*cpErd*rhoErd/(4*lambdaErd);
  STrt0=4*M_PI*lambdaErd*Sondenlaenge/DimAxi;
  STrt= 0;
  for(i= 1; i<Woche+1; i++) {
    u=u0/(i*604800*RepRandbed);
    if (u > 1)STrt = 0;
    else {
      W=-0.5772-log(u);
      j=1;
      W_alt=W-hoch(-1,j)*hoch(u,j)/(j*Fakultaet(j));
      W=W_alt;
      do {
	W_alt=W;
	j=j+1;
	W=W-hoch(-1,j)/j*hoch(u,j)/(Fakultaet(j));
      }
      while (fabsl(1-W/W_alt) >= 0.01);
      STrt = STrt+(-Q[k][Woche-i+1]+Q[k][Woche-i])/STrt0*W;
    };
  };
  return STrt;
}

static double hoch(double a, long b) // a^b
{
  if(a>0) return exp(b * log(a));
  else if(b%2 == 1) return -exp(b * log(-a));
  else return exp(b * log(-a));
}
static long Fakultaet(int x)
{
  long i,y;
  y=1;
  for(i=1; i<=x; i++)
    y=y*i;
  return y;
}
