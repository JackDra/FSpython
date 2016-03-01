#!/usr/bin/env python

from RunParams import *
import os

def SortConfigs(setfilelist):
    sortlist = [int(iset.split('.')[-1]) for iset in setfilelist]
    doublist = sorted(zip(setfilelist,sortlist),key=lambda k : k[1])
    return [ia for ia,ib in doublist]

def CreateCfgList(thisgfosnum):
    setcfg = thisgfosnum + 4
    if setcfg > 9:
        setcfg += -10
    print 'gf set number ',thisgfosnum,' corresponds to config pref number ', setcfg
    filelist = os.listdir(rdsigfdir)
    setfilelist = []
    for ifile in filelist:
        if str(setcfg)+'.lime' in ifile:
            setfilelist.append('.'+'.'.join(ifile.split('.')[1:3])+'\n')
    setfilelist = SortConfigs(setfilelist)
    thisfile = open(filelists+CreateCfgFilename(thisgfosnum),'w')
    thisfile.writelines(setfilelist)
    thisfile.close()
    return setfilelist
    

def GetIcfgTOFcfg(nproc,nconf):
    confbreak = nconf/nproc
    outarray = []
    for istart,iend in zip(range(1,nconf+1,confbreak),range(confbreak,nconf+1+confbreak,confbreak)):
        outarray.append((istart,iend))
    return outarray
