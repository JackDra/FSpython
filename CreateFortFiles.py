#!/usr/bin/env python

from RunParams import *
from FilenameFuns import *
import os

def makeqlist(Minqsqrd,Maxqsqrd):
    qlist = []
    for iq1 in range(-Maxqsqrd,Maxqsqrd+1):
        for iq2 in range(-Maxqsqrd,Maxqsqrd+1):
            for iq3 in range(-Maxqsqrd,Maxqsqrd+1):
                if iq1**2 + iq2**2 + iq3**2 > Maxqsqrd: continue
                if iq1**2 + iq2**2 + iq3**2 < Minqsqrd: continue
                qlist.append(str(iq1) + ' ' + str(iq2) + ' ' + str(iq3))
    return qlist

def Remove2ptPropFiles(folder,fileprefix,icfg,thisgfosnum,thisismlist):
    for ism in map(str,thisismlist):
        thisfile = folder+'/prop2pt'+ism+'/'+fileprefix+str(icfg)+'S'+str(thisgfosnum)
        if os.path.isfile(thisfile+'.lat'):os.remove(thisfile+'.lat')
        if os.path.isfile(thisfile+'.qpsrc_sm'):os.remove(thisfile+'.qpsrc_sm')
        if os.path.isfile(thisfile+'.quarkprop'):os.remove(thisfile+'.quarkprop')
        if os.path.isfile(thisfile+'.fm_slinc'):os.remove(thisfile+'.fm_slinc')

def Create2ptPropFiles(folder,fileprefix,icfg,thisgfosnum,thisismlist):
    filelistsm = []
    for ism in map(str,thisismlist):
        mkdir_p(folder+'/prop2pt'+ism+'/')
        thisfile = folder+'/prop2pt'+ism+'/'+fileprefix+str(icfg)+'S'+str(thisgfosnum)
        filelistsm.append(FortFolderPref+'/'+thisfile.replace(folder+'/',''))
        f = open(thisfile+'.lat','w')
        f.write(str(nx)+'\n')
        f.write(str(nx)+'\n')
        f.write(str(nx)+'\n')
        f.write(str(nt)+'\n')
        f.close()

        f = open(thisfile+'.qpsrc_sm','w')
        f.write(str(ix)+'\n')
        f.write(str(ix)+'\n')
        f.write(str(ix)+'\n')
        f.write(str(it)+'\n')
        f.write('1\n')
        f.write(str(ism)+'\n')
        f.write('1\n')
        f.write(str(alpha)+'\n')
        f.write('f\n')
        f.write(str(u0)+'\n')
        f.write(str(StoutLink)+'\n')
        f.write(str(alphaStout)+'\n')
        f.write(str(gfsweeps)+'\n')
        f.close()

        f = open(thisfile+'.quarkprop','w')
        f.write(gfdir+CreateCfg(icfg,thisgfosnum)+'\n')
        f.write(GrpFormat+'\n')
        f.write(qpdir+CreateCfg(icfg,thisgfosnum)+'.t'+str(it)+'sm'+str(ism)+'\n')
        f.write(PropFormat+'\n')
        f.write(ParrIO+'\n')
        f.write('slinc\n')
        f.write('0.'+str(kud)+'\n')
        f.write(' '.join(map(str,[SRCX[thisgfosnum], SRCY[thisgfosnum], SRCZ[thisgfosnum], SRCT[thisgfosnum]]))+'\n')
        f.write('0\n')
        f.write(str(Prec)+'\n')
        f.write(str(SourceType)+'\n')
        f.close()

        f = open(thisfile+'.fm_slinc','w')
        f.write(str(bx)+'\n')
        f.write(str(by)+'\n')
        f.write(str(bz)+'\n')
        f.write(str(bt)+'\n')
        f.write(str(u0)+'\n')
        f.write(str(csw)+'\n')
        f.write(str(rho)+'\n')
        f.write(str(nstout)+'\n')
        f.close()
    return filelistsm


def Remove2ptCorrFiles(folder,fileprefix,icfg,thisgfosnum,thisismlist):
    for ism in map(str,thisismlist):
        thisfile = folder+'/corr2pt'+ism+'/'+fileprefix+str(icfg)+'S'+str(thisgfosnum)
        if os.path.isfile(thisfile+'.lat'):os.remove(thisfile+'.lat')
        if os.path.isfile(thisfile+'.interp'):os.remove(thisfile+'.interp')
        if os.path.isfile(thisfile+'.mom'):os.remove(thisfile+'.mom')
        if os.path.isfile(thisfile+'.prop_sm'):os.remove(thisfile+'.prop_sm')
        if os.path.isfile(thisfile+'.cfun'):os.remove(thisfile+'.cfun')
        if os.path.isfile(thisfile+'.prop'):os.remove(thisfile+'.prop')
        if os.path.isfile(thisfile+'.gf'):os.remove(thisfile+'.gf')
        if os.path.isfile(thisfile+'.gfshift'):os.remove(thisfile+'.gfshift')


def Create2ptCorrFiles(folder,fileprefix,icfg,thisgfosnum,thisismlist):
    filelistsm = []
    thisqlist = makeqlist(qmin,qmax)
    for ism in map(str,thisismlist):
        mkdir_p(folder+'/corr2pt'+ism+'/')
        thisfile = folder+'/corr2pt'+ism+'/'+fileprefix+str(icfg)+'S'+str(thisgfosnum)
        filelistsm.append(FortFolderPref+'/'+thisfile.replace(folder+'/',''))
        f = open(thisfile+'.lat','w')
        f.write(str(nx)+'\n')
        f.write(str(nx)+'\n')
        f.write(str(nx)+'\n')
        f.write(str(nt)+'\n')
        f.close()

        f = open(thisfile+'.interp','w')
        f.write('[pi]\n')
        f.write('0\n')
        f.write('1\n')
        f.write('1.0 * ( d g5 u )\n')
        f.write('[nucleon]\n')
        f.write('1\n')
        f.write('1\n')
        f.write('1.0 * ( u Cg5 d ) I u\n')
        f.write('[delta]\n')
        f.write('2\n')
        f.write('2\n')
        f.write('2.0/sqrt(3.0) * ( u Cgmu d ) I u\n')
        f.write('1.0/sqrt(3.0) * ( u Cgmu u ) I d\n')
        f.close()
        
        f = open(thisfile+'.mom','w')
        f.write(str(len(thisqlist))+'\n')
        for iq in thisqlist:
            f.write(iq+'\n')
        f.close()

        f = open(thisfile+'.prop_sm','w')
        f.write(str(alpha)+'\n')
        f.write(str(smu0)+'\n')
        f.write(str(len(jsmlist))+'\n')
        for jsm in map(str,jsmlist):
            f.write(str(jsm)+'\n')
        f.write(gfdir+CreateCfg(icfg,thisgfosnum)+'\n')
        f.write(GrpFormat+'\n')
        f.write(str(gfsweeps)+'\n')
        f.write(StoutLink+'\n')
        f.write(str(alphaStout)+'\n')
        f.close()

        f = open(thisfile+'.cfun','w')
        f.write(cfdir+'source'+str(thisgfosnum)+'/'+CreateCfg(icfg,thisgfosnum)+'.t'+str(it)+'sm'+ism+'k'+str(kud)+'.'+PropFormat+'\n')
        f.write(MCTFormat+'\n')
        f.write('T\n')
        f.write(str(Ustar)+'\n')
        f.write(str(gamma_rep)+'\n')
        f.write('0\n')
        f.write('1\n')
        f.write('nucleon\n')
        f.close()

        f = open(thisfile+'.prop','w')
        f.write(PropFormat+'\n')
        f.write(parallelIO+'\n')
        f.write(str(sinksmear)+'\n')
        f.write(Get2ptProp(icfg,thisgfosnum,ism)+'\n')
        f.close()

        f = open(thisfile+'.gf','w')
        f.write(gfdir+CreateCfg(icfg,thisgfosnum)+'\n')
        f.write(GrpFormat+'\n')
        f.close()

        f = open(thisfile+'.gfshift','w')
        f.write(' '.join(map(str,[SRCX[thisgfosnum], SRCY[thisgfosnum], SRCZ[thisgfosnum], SRCT[thisgfosnum]]))+'\n')
        f.close()
    return filelistsm


def Remove3ptCorrFiles(folder,fileprefix,icfg,thisgfosnum,thisismlist,thisDSList,thisProjectorList,thisit_sst):
    for ism in map(str,thisismlist):
        for DS in thisDSList:
            for Projector in map(str,thisProjectorList):
                for iTS in map(str,thisit_sst):                    
                    thisfolder = folder+'/corr3pt'+ism+'/'+DS+'GMA'+Projector+'tsink'+iTS+'/'
                    thisfile = thisfolder+fileprefix+str(icfg)+'S'+str(thisgfosnum)
                    if os.path.isfile(thisfile+'.lat'):os.remove(thisfile+'.lat')
                    if os.path.isfile(thisfile+'.qpsrc_sm'):os.remove(thisfile+'.qpsrc_sm')
                    if os.path.isfile(thisfile+'.fm_slinc'):os.remove(thisfile+'.fm_slinc')
                    if os.path.isfile(thisfile+'.quarkprop'):os.remove(thisfile+'.quarkprop')
                    if os.path.isfile(thisfile+'.qpsrc_cmfs'):os.remove(thisfile+'.qpsrc_cmfs')


def Create3ptCorrFiles(folder,fileprefix,icfg,thisgfosnum,thisismlist,thisDSList,thisProjectorList,thisit_sst):
    filelistsm = []
    for ism in map(str,thisismlist):
        for DS in thisDSList:
            for Projector in map(str,thisProjectorList):
                for iTS in map(str,thisit_sst):                    
                    thisfolder = folder+'/corr3pt'+ism+'/'+DS+'GMA'+Projector+'tsink'+iTS+'/'
                    mkdir_p(thisfolder)
                    thisfile = thisfolder+fileprefix+str(icfg)+'S'+str(thisgfosnum)
                    filelistsm.append(FortFolderPref+'/'+thisfile.replace(folder+'/',''))
                    f = open(thisfile+'.lat','w')
                    f.write(str(nx)+'\n')
                    f.write(str(nx)+'\n')
                    f.write(str(nx)+'\n')
                    f.write(str(nt)+'\n')
                    f.close()
        
        
                    f = open(thisfile+'.qpsrc_sm','w')
                    f.write(str(ix)+'\n')
                    f.write(str(ix)+'\n')
                    f.write(str(ix)+'\n')
                    f.write(str(it)+'\n')
                    f.write('1\n')
                    f.write(str(ism)+'\n')
                    f.write('1\n')
                    f.write(str(alpha)+'\n')
                    f.write('f\n')
                    f.write(str(u0)+'\n')
                    f.write(str(StoutLink)+'\n')
                    f.write(str(alphaStout)+'\n')
                    f.write(str(gfsweeps)+'\n')
                    f.close()

                    f = open(thisfile+'.fm_slinc','w')
                    f.write(str(bx)+'\n')
                    f.write(str(by)+'\n')
                    f.write(str(bz)+'\n')
                    f.write(str(bt)+'\n')
                    f.write(str(u0)+'\n')
                    f.write(str(csw)+'\n')
                    f.write(str(rho)+'\n')
                    f.write(str(nstout)+'\n')
                    f.close()

                    f = open(thisfile+'.quarkprop','w')
                    f.write(gfdir+CreateCfg(icfg,thisgfosnum)+'\n')
                    f.write(GrpFormat+'\n')
                    f.write('F\n')
                    thisREvecDir = REvecFlag+'sm'+str(ism)+REvecFlag+'nD'+str(PoFShifts)+'GMA'+str(Projector)+'t'+str(iTS)+'p'+''.join(map(str,ppvec))+'.'+DS+'/'
                    f.write(CreateCfdir3pt(thisgfosnum)+thisREvecDir+CreateCfg(icfg,thisgfosnum)+'.t'+str(it)+'sm'+ism+REvecFlag+'nD'+str(PoFShifts)+
                            'GMA'+Projector+'t'+iTS+'p'+''.join(map(str,ppvec))+'.'+DS+'\n')
                    f.write(PropFormat+'\n')
                    f.write(ParrIO+'\n')
                    f.write(GammaRep+'\n')
                    f.write(str(qmin)+'\n')
                    f.write(str(qmax)+'\n')
                    f.write(str(NDer)+'\n')
                    f.write('slinc\n')
                    f.write('0.'+str(kud)+'\n')
                    f.write(' '.join(map(str,[SRCX[thisgfosnum], SRCY[thisgfosnum], SRCZ[thisgfosnum], SRCT[thisgfosnum]]))+'\n')
                    f.write('0\n')
                    f.write(str(Prec)+'\n')
                    f.write(str(CMFSSourceType)+'\n')
                    f.close()
                    
                    f = open(thisfile+'.qpsrc_cmfs','w')
                    f.write(Get2ptProp(icfg,thisgfosnum,ism)+'\n')
                    f.write(ism+'\n')
                    f.write(str(it)+'\n')
                    f.write('0.'+str(kud)+'\n')
                    f.write(Projector+'\n')
                    f.write(iTS+'\n')
                    f.write('1 1 1\n')
                    f.write(' '.join(map(str,ppvec))+'\n')
                    f.write('6\n')
                    f.write(str(len(jsmlist))+'\n')
                    f.write(str(PoFShifts)+'\n')
                    for jsm in jsmlist:
                        f.write(str(jsm)+'\n')
                    for iRVec in RVec:
                        f.write(str(iRVec)+'\n')
                    f.write(str(alpha)+'\n')
                    f.write('f\n')
                    f.write(str(u0)+'\n')
                    f.write(str(StoutLink)+'\n')
                    f.write(str(alphaStout)+'\n')
                    f.write(str(gfsweeps)+'\n')
                    f.write(str(Projector)+'\n')
                    f.write(str(DS)+'\n')
                    f.close()
    return filelistsm

