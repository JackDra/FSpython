#!/usr/bin/env python

from RunParams import *
from CreateCfgFile import *
from CreateFortFiles import *
from GetAndCheckData import *
from ReSubmit import RunNext
import sys
import subprocess

if len(sys.argv) != 3:
    raise IOError('Please give set number and number of processors')

if sys.argv[2] == 'a':
    thisgfosnum = range(1,10)
else:
    thisgfosnum = map(int,sys.argv[2:])
nproc = int(sys.argv[1])

nproc = nproc/len(thisgfosnum)


for igfos in thisgfosnum:
    thiscfglist = CreateCfgList(igfos)
    cfgintervals = GetIcfgTOFcfg(nproc,len(thiscfglist))
    for icfg,fcfg in cfgintervals:
        print 'Submitting source'+str(igfos)+' icfg='+str(icfg)+' fcfg='+str(fcfg)
        RunNext(icfg,fcfg,igfos,Start=True)
