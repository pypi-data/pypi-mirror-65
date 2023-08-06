#include "pascal_defs.h"

void multiplizieren (KMatrix M, Matrix w, Matrix y,
		     int k, int DimRad)
{
  /*    ***********    y = M x w       ************   */
  int i,j;
  y[k][0] = w[k][0];
  y[k][DimRad+1] = w[k][DimRad+1];
  for(i=1; i<=DimRad; i++)
    {
      y[k][i] = 0;
      for(j=0; j<=DimRad+1; j++) y[k][i]=y[k][i] + M[k][i][j] * w[k][j];
    }
}
