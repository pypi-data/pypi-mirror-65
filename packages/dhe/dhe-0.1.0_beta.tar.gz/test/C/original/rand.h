#ifndef __RAND_H__
#define __RAND_H__

#include "pascal_defs.h"

double RandAussen_gfunc(int k, int Woche,
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
			double u_min);

double RandAussen(int k, int Woche,
		  int Zeitschritt, long simstep,
		  int RepRandbed,
		  MatrixQ Q,
		  double cpErd,double rhoErd,double lambdaErd,
		  double Rechenradius,double Sondenlaenge,
		  int DimAxi);

#endif //__RAND_H__
