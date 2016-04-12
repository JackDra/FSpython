Made for submitting Jobs on a SLURM system for running Jacks Modified COLA code.

Please go through wholefile and substitute with own parameters:
       
       RunParams.py

Check SLURM submission parameters for:
      
      Run2ptProp.csh, Run2ptCorr.csh and Run3ptCorr.csh

need to change in above:
 
	#SLURM  headers
	module load stuff
	curdir
	colanewgpu
	reportfolder
	

