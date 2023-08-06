//from .pascal_defs import Vektor10, Vektor, Matrix
#include "pascal_defs.h"
#include "tbrine.h"

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
  // var i, k: integer
  //    TOut, dt2, Lm0, Lm1, LmMin, L0mcpdt, Nichtad: float
{
  Vektor SummeT;
  Vektor Td;
  Vektor Tu;
  Vektor dTa;
  double dt2 = Zeitschritt * 60. / subdt / substep;  // [s]
  TDown[0] = TSink;
  double TOut = 0;
  double L0mcpdt = L0 / mcpSole * dt2;
  int i, _step;
  for(i=1; i<DimAxi + 1;i++)
    SummeT[i] = 0;
  for(_step=1; _step<substep + 1; _step++)
    {
      if(KoaxialSonde)  // KoaxialSonde: Neu 10.1.2000
	{
	  for(i=1; i<DimAxi + 1; i++)
	    {
	      Td[i] = (T[i][1] - TDown[i]) * L[i] / mcpSoleDown * dt2;
	      if(stationaer)
		TDown[i] = (L[i] * T[i][1] + L0 * TDown[i - 1] +
			    La[i] * TUp[1 + DimAxi - i]) / (L[i] + L0 + La[i]);
                else
		  {
                    dTa[i] = (TUp[1 + DimAxi - i] - TDown[i]);
                    TDown[i] = TDown[i] + \
                        (TDown[i - 1] - TDown[i]) * L0 / mcpSoleDown * dt2 \
		      + dTa[i] * La[i] / mcpSoleDown * dt2 + Td[i];
		  }
	      Td[i] = (T[i][1] - TDown[i]) * L[i] / mcpSoleDown * dt2;
	    }
	  TUp[0] = TDown[DimAxi];
	  for(i=1; i<DimAxi + 1; i++)
	    {
	      if(stationaer)
		TUp[i] = (La[1 + DimAxi - i] * TDown[1 + DimAxi - i] +
			  L0 * TUp[i - 1]) / (La[1 + DimAxi - i] + L0);
	      else
		TUp[i] = TUp[i] + (TUp[i - 1] - TUp[i]) *	\
		  L0 / mcpSoleUp * dt2				\
		  - dTa[1 + DimAxi - i] *			\
		  La[1 + DimAxi - i] / mcpSoleUp * dt2;
	      // dTa[1 + DimAxi - 1] -> dTa[1 + DimAxi - i]
	    }
	  for(i=1;i< DimAxi + 1;i++)
	    SummeT[i] = SummeT[i] + Td[i];
	  TOut = TOut + TUp[DimAxi];
	  // Koaxialsonde: # Ende des neuen Teils
	}
      else  // doppel - U - Sonde
	{
	  for(i=1;i< DimAxi + 1;i++)
	    {
	      Td[i] = (T[i][1] - TDown[i]) * L[i] / 2 / mcpSole * dt2;
		if(stationaer)
		  TDown[i] = (L[i] / 2 * T[i][1] + L0 *
			      TDown[i - 1]) / (L[i] / 2 + L0);
                else
		  TDown[i] = TDown[i] +					\
		    (TDown[i - 1] - TDown[i]) * L0mcpdt + Td[i];
	      Td[i] = (T[i][1] - TDown[i]) * L[i] / 2 / mcpSole * dt2;
	    }
	  TUp[0] = TDown[DimAxi];
	  for(i=1;i< DimAxi + 1;i++)
	    {
	      Tu[i] = (T[1 + DimAxi -i][1] - TUp[i]) *		\
		L[1 + DimAxi - i] / 2 / mcpSole * dt2;
	      if(stationaer)
		TUp[i] = (L[1 + DimAxi - i] / 2 * T[1 + DimAxi - i][1] +
			  L0 * TUp[i - 1]) / (L[1 + DimAxi - i] / 2 + L0);
	      else
		TUp[i] = TUp[i] +				\
		  (TUp[i - 1] - TUp[i]) * L0mcpdt + Tu[i];
	      Tu[i] = (T[1 + DimAxi - i][1] - TUp[i]) *		\
		L[1 + DimAxi - i] / 2 / mcpSole * dt2;
	    }
	  for(i=1;i< DimAxi + 1;i++)
	    SummeT[i] = SummeT[i] + Td[i] + Tu[1 + DimAxi - i];
	  TOut = TOut + TUp[DimAxi];
	}//(*** Ende Doppel - U - Sonde ** ***********************)
    }
  if(KoaxialSonde)
    for(i=1;i< DimAxi + 1;i++)
      QWand[i] = SummeT[i] * mcpSoleDown;
  else
    for(i=1;i< DimAxi + 1;i++)
      QWand[i] = SummeT[i] * mcpSole;
  TOut = TOut / substep;
  return TOut;
}
