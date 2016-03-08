#!/usr/bin/env python

from RunParams import *
from GetAndCheckData import *
from CreateFortFiles import *
import sys
import subprocess
import commands

DefParams = [it_sst[0],ProjectorList[0],DSList[0]]

def IncrementRun(stage,ism,tsink,Projector,DS):
    if 'twoptprop' in stage:
        stage = 'twoptcorr'
        return [stage,ism]+DefParams
    if 'twoptcorr' in stage:
        stage = 'threeptcorr'
        return [stage,ism]+DefParams
    if 'threeptcorr' in stage:
        if tsink == it_sst[-1]:
            if Projector == ProjectorList[-1]:
                if DS == DSList[-1]:
                    if ism == ismlist[-1]:
                        stage,ism,tsink,Projector,DS = ['Done',ismlist[0]]+DefParams
                    else:
                        stage,ism,tsink,Projector,DS = ['twoptprop',ismlist[ismlist.index(ism)+1]]+DefParams
                else:
                    tsink = it_sst[0]
                    Projector = ProjectorList[0]                    
                    DS = DSList[DSList.index(DS)+1]
            else:
                tsink = it_sst[0]
                Projector = ProjectorList[ProjectorList.index(Projector)+1]
        else:
            tsink = it_sst[it_sst.index(tsink)+1]
        return stage,ism,tsink,Projector,DS

def RunNext(icfg,fcfg,gfos,stage='twoptprop',ism=ismlist[0],tsink=it_sst[0],Projector=ProjectorList[0],DS=DSList[0],Start=False):
    icfg,fcfg,gfos,ism,tsink,Projector = map(int,[icfg,fcfg,gfos,ism,tsink,Projector])
    #removes fort parameter files
    if 'twoptprop' in stage:
        Remove2ptPropFiles(FortFolder,FortFileFlag,icfg,gfos,[ism])    
    elif 'twoptcorr' in stage:
        Remove2ptCorrFiles(FortFolder,FortFileFlag,icfg,gfos,[ism])    
    elif 'threeptcorr' in stage:
        Remove3ptCorrFiles(FortFolder,FortFileFlag,icfg,gfos,[ism],[DS],[Projector],[tsink])    
        
    #check if whole run is done
    
    if Check2ptCorr(icfg,gfos,[ism],jsmlist) and Check3ptCorr(icfg,gfos,[ism],it_sst,ProjectorList,DSList):
        RemoveProp(icfg,gfos,[ism])
        if ism == ismlist[-1]:
            RemoveGaugeField(icfg,gfos)
            if icfg<fcfg:
                RunNext(icfg+1,fcfg,gfos,Start=True)
                return 
            else:
                print 'All Complete'
        else:
            RunNext(icfg,fcfg,gfos,ism=ismlist[ismlist.index(ism)+1],Start=Start)
            return

    GetGaugeField(icfg,gfos)
    Move2ptCorr(icfg,gfos,[ism],jsmlist)
    prevism = ism
    if not Start: stage,ism,tsink,Projector,DS = IncrementRun(stage,ism,tsink,Projector,DS)
        
    StillInc = True
    while StillInc:
        StillInc = False
        if 'twoptprop' in stage:
            if Check2ptProp(icfg,gfos,[ism]):
                stage,ism,tsink,Projector,DS = IncrementRun(stage,ism,tsink,Projector,DS)
                StillInc = True
        elif 'twoptcorr' in stage:
            Move2ptCorr(icfg,gfos,[ism],jsmlist)
            if Check2ptCorr(icfg,gfos,[ism],jsmlist):
                stage,ism,tsink,Projector,DS = IncrementRun(stage,ism,tsink,Projector,DS)
                StillInc = True
        elif 'threeptcorr' in stage:
            if Check3ptCorr(icfg,gfos,[ism],[tsink],[Projector],[DS]):
                stage,ism,tsink,Projector,DS = IncrementRun(stage,ism,tsink,Projector,DS)
                if 'Done' not in stage: StillInc = True
    if prevism != ism:
        RemoveProp(icfg,gfos,[prevism])

    if 'twoptprop' in stage:
        [thisjobid] = Create2ptPropFiles(FortFolder,FortFileFlag,icfg,gfos,[ism])    
        Jstring = str(icfg)+'-'+str(fcfg)+'-S'+str(gfos)+'-sm'+str(ism)
        sbatchstring = ('sbatch -J '+Jstring+' --export=ALL,gfos='+str(gfos)+',ism='+str(ism)+
                        ',icfg='+str(icfg)+',fcfg='+str(fcfg)+',jobid='+str(thisjobid)+',mach='+str(thismachine)+' '+str(scriptdir)+'Run2ptProp.csh')
        print sbatchstring
        subprocess.call(sbatchstring.split(),cwd=basedir)
    elif 'twoptcorr' in stage:
        [thisjobid] = Create2ptCorrFiles(FortFolder,FortFileFlag,icfg,gfos,[ism])    
        Jstring = str(icfg)+'-'+str(fcfg)+'-S'+str(gfos)+'-sm'+str(ism)
        sbatchstring = ('sbatch -J '+Jstring+' --export=ALL,gfos='+str(gfos)+',ism='+str(ism)+
                        ',icfg='+str(icfg)+',fcfg='+str(fcfg)+',jobid='+str(thisjobid)+',mach='+str(thismachine)+' '+str(scriptdir)+'Run2ptCorr.csh')
        print sbatchstring
        subprocess.call(sbatchstring.split(),cwd=basedir)
    elif 'threeptcorr' in stage:
        [thisjobid] = Create3ptCorrFiles(FortFolder,FortFileFlag,icfg,gfos,[ism],[DS],[Projector],[tsink])    
        mkdir_p(Get3ptCorrFolder(icfg,gfos,ism,tsink,Projector,DS))
        Jstring = str(icfg)+'-'+str(fcfg)+'-S'+str(gfos)+'-sm'+str(ism)+'-ts'+str(tsink)+'-P'+str(Projector)+'-'+DS[0]
        sbatchstring = ('sbatch -J '+Jstring+' --export=ALL,gfos='+str(gfos)+',ism='+str(ism)+
                        ',tsink='+str(tsink)+',Projector='+str(Projector)+',DS='+str(DS)+
                        ',icfg='+str(icfg)+',fcfg='+str(fcfg)+',jobid='+str(thisjobid)+',mach='+str(thismachine)+' '+str(scriptdir)+'Run3ptCorr.csh')
        print sbatchstring
        subprocess.call(sbatchstring.split(),cwd=basedir)
    elif 'Done' in stage:
        if icfg<fcfg:
            RunNext(icfg+1,fcfg,gfos,Start=True)
        else:
            print 'All Complete'
        

if len(sys.argv) > 1 and 'ReSubmit' in sys.argv[0]:
    RunNext(*sys.argv[1:])
