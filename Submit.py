#!/usr/bin/env python

from RunParams import *
from CreateCfgFile import *
from CreateFortFiles import *
from GetAndCheckData import *
from ReSubmit import RunNext
import sys
import subprocess

thisgfosnum = range(1,10)
nproc = -1
for iin in sys.argv[1:]:
    if '-np=' in iin:
        nproc = int(iin.replace('-np=',''))
    elif '-s=' in iin:
        thisgfosnum = map(int,iin.replace('-s=','').split(','))

if nproc == -1:
    raise IOError('please give number of processors as -np=## ')
    
print 'Sources = ' , ','.join(map(str,thisgfosnum))
print 'Number of processors = ' , nproc

# if sys.argv[2] == 'a':
#     thisgfosnum = range(1,10)
# else:
#     thisgfosnum = map(int,sys.argv[2:])
# nproc = int(sys.argv[1])

nproc = nproc/len(thisgfosnum)


for igfos in thisgfosnum:
    thiscfglist = CreateCfgList(igfos)
    cfgintervals = GetIcfgTOFcfg(nproc,len(thiscfglist))
    for icfg,fcfg in cfgintervals:
        print 'Submitting source'+str(igfos)+' icfg='+str(icfg)+' fcfg='+str(fcfg)
        RunNext(icfg,fcfg,igfos,Start=True)
