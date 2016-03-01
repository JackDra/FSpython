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

thisgfosnum = int(sys.argv[1])
nproc = int(sys.argv[2])

thiscfglist = CreateCfgList(thisgfosnum)

cfgintervals = GetIcfgTOFcfg(nproc,len(thiscfglist))

for icfg,fcfg in cfgintervals:
    RunNext(icfg,fcfg,thisgfosnum,Start=True)
