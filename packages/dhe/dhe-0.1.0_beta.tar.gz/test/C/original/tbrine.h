#ifndef __TBRINE_H__
#define __TBRINE_H__

#include "pascal_defs.h"

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
	      );

#endif //__TBRINE_H__
