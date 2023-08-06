#include <stdbool.h>
#include "pascal_defs.h"
#include "tbrine.h"
#include "rand.h"
#include "multiplizieren.c"

void WriteStep(int filestep, double Massenstrom, double TSink, double QSource,
	       double TSource,
	       double TEarth,
	       double p, _Bool laminar);
void ReadStep(int filestep, double Massenstrom, double TSink, double QSource);

double calculateEWS(int Iteration, int DimAxi, int DimRad,
		  int MonitorAxi,
		  int MonitorRad,
		  Matrix TEarthOld,
		  Matrix TEarth,
		  Vektor TUp,
		  Vektor TUpOld,
		  Vektor TDownOld,
		  Vektor TDown,
		  Vektor Q0Old,
		  Vektor Q0,
		  double TSourceOld,
		  double TSource,
		  double TSourceMin,
		  double TSourceMax,
		  double TSink,
		  double TSinkMin,
		  double TSinkMax,
		  double QSource,
		  double Massenstrom,
		  double cpSole,
		  double p,
		  _Bool laminar,
		  _Bool readFile,
		  int simstep,
		  int StepWrite,
		  _Bool einschwingen,
		  _Bool Allsteps,
		  _Bool writeFile,
		  _Bool Leistung,
		  _Bool gfunction,
		 int RepRandbed,
                 int Zeitschritt,
                 int Jahr,
                 long numrows,
                 _Bool Starttemp, 
                 double DeltaT,
                 int Subdt,
                 int AnzahlSonden,
                 double Rechenradius,
                 _Bool Stationaer,
		  double mcpSole,
		  int substep_run,
		  Vektor L1run,
                 int substep_stop,
                 Vektor L1stop,
                 Vektor10 lambdaErde,
                 Vektor10 rhoErde,
                 Vektor10 cpErde,
                 MatrixQ Q,
                 Vektor T0,
                 KMatrix B1, KMatrix B2,
                 Matrix Tneu,
                 double gpar6,
                 double gpar5,
                 double gpar4,
                 double gpar3,
                 double gpar2,
                 double gpar1,
                 double Sondenlaenge,
                 double TMonitor,
                 double u_min)
{
      int i,j,idt;
      int filestep, Woche, simstepn;
      double Summe_TSource, L0, TRT;
      _Bool Pumpelauft;
      Vektor QWand;
      {
	 if (Iteration == 0){
	    for(i=1; i<DimAxi+1; i++) {
	       for(j=1; j<DimRad+1; j++) TEarthOld[i][j] = TEarth[i][j];
	       TUpOld[i]    = TUp[i];
	       TDownOld[i] = TDown[i];
	       Q0Old[i]     = Q0[i];
	    }
	 } else {
	    for(i=1; i<DimAxi+1; i++) {
	       for(j=1; j<DimRad+1; j++) TEarth[i][j] = TEarthOld[i][j];
	       TUp[i]    = TUpOld[i];
	       TDown[i] = TDownOld[i];
	       Q0[i]     = Q0Old[i];
	    };
	 };
	 
	 if (Iteration == 0){
	    if (! readFile)filestep=simstep-1;
	    if (simstep>1)if (((! einschwingen) || Allsteps)) {
	       if (TSource < TSourceMin)TSourceMin = TSource;
	       if (TSource > TSourceMax)TSourceMax = TSource;
	       if (TSink < TSinkMin)TSinkMin = TSink;
	       if (TSink > TSinkMax)TSinkMax = TSink;
	       if (writeFile)
		 if (((simstep-1) % StepWrite) == 0) {
		   if (Leistung)if (Massenstrom>0.0001)
				  TSink = TSource-QSource*1000/Massenstrom/cpSole;
		     else TSink = TSource;
		   else QSource= (TSource-TSink)*Massenstrom*cpSole/1000;
		   WriteStep(filestep,Massenstrom,TSink,QSource,TSource,
			     TEarth[MonitorAxi][MonitorRad],p,laminar);
		 };
	      };
	    if (readFile)ReadStep(filestep,Massenstrom,TSink,QSource);
	    if (DeltaT!=0)TSink = TSourceOld - DeltaT;
	 };
	 
	 if (Iteration >-1){
	    Summe_TSource = 0;
	    if (! Starttemp){
	       Woche    = (simstep+numrows*(Jahr-1)-1) / (10080 / Zeitschritt * RepRandbed) + 1;
	       simstepn= (simstep+numrows*(Jahr-1)) % (10080 / Zeitschritt * RepRandbed);
	    } else {
	       Woche    = (simstep-1) / (10080 / Zeitschritt * RepRandbed) + 1;
	       simstepn= (simstep) % (10080 / Zeitschritt * RepRandbed);
	    };
	    if (simstepn  ==  0)simstepn = 10080 / RepRandbed / Zeitschritt;
	    // Rechengebiet = Rechenradius - Bohrdurchmesser / 2;
	    L0              = cpSole * Massenstrom / AnzahlSonden;
	    if (Massenstrom>0.00001) Pumpelauft = true; else Pumpelauft = false;
	    for(idt = 1; idt <Subdt+1; idt ++) {
	       //  calculate brine Temperature 
	       if (Pumpelauft){
		 TSource = TBRINE(TEarth,TDown,TUp,TSink,L0, L1run, 0/*La*/, Zeitschritt,Subdt,
				  substep_run,QWand,mcpSole,0./*mcpSoleUp*/,0./*mcpSoleDown*/,DimAxi,Stationaer, false/*KoaxialSonde*/);
		  for(i= 1; i<DimAxi+1; i++) TEarth[i][0]=TEarth[i][1]
		     - QWand[i]/L1run[i]/Zeitschritt/60.*Subdt;
	       } else {
		 TSource = TBRINE(TEarth,TDown,TUp,0,0,L1stop,0/*La*/,Zeitschritt,Subdt,
				  substep_stop,QWand,mcpSole,0./*mcpSoleUp*/,0./*mcpSoleDown*/,DimAxi,Stationaer, false/*KoaxialSonde*/);
		  for(i= 1; i<DimAxi+1; i++) TEarth[i][0]=TEarth[i][1]
		     - QWand[i]/L1stop[i]/Zeitschritt/60.*Subdt;
	       };
	       for(i=1; i<DimAxi+1; i++) {
		  //  calculate temperature at outer boudary condition at each RepRandBed 
		  Q0[i] = (Q0[i] * ((simstepn-1)*Subdt + (idt-1))
			    + QWand[i]*Subdt/Zeitschritt/60.)/((simstepn-1)*Subdt+idt);
		  if (Iteration == 0){
		     if (idt == Subdt){
			if (((simstep+numrows*(Jahr-1))*Zeitschritt) % (60*24*7*RepRandbed)  ==  0){
			   Q[i][Woche] = Q0[i];
			   if (gfunction)
			      TRT = RandAussen_gfunc(i,Woche,Zeitschritt,(simstep+numrows*(Jahr-1)),
						     RepRandbed,Q,cpErde[i],rhoErde[i],lambdaErde[i],Rechenradius,
						     Sondenlaenge,gpar1,gpar2,gpar3,gpar4,gpar5,gpar6,DimAxi, u_min);
			   else
			      TRT = RandAussen(i,Woche,Zeitschritt,(simstep+numrows*(Jahr-1)),RepRandbed,
					       Q,cpErde[i],rhoErde[i],lambdaErde[i],Rechenradius,Sondenlaenge,DimAxi);
			   TEarth[i][DimRad+1] = T0[i] + TRT;
			};
		     };
		  };
		  //  calulate earth temperature       
		  if (Pumpelauft)multiplizieren(B1,TEarth,Tneu,i,DimRad);
		  else multiplizieren(B2,TEarth,Tneu,i,DimRad);
		  for(j=1; j<DimRad+1; j++) TEarth[i][j] = Tneu[i][j];
	       }
	       Summe_TSource = Summe_TSource + TSource;
	    }
	    TSource = Summe_TSource / Subdt;          //  avarage source temperature 
	    TSourceOld = TSource;
	    TMonitor = TEarth[MonitorAxi][MonitorRad];
	 }
      }
      return TSource;
}
