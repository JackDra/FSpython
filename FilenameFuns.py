#!/usr/bin/env python 

from RunParams import *

def Get2ptProp(icfg,thisgfosnum,ism):
    return qpdir+CreateCfg(icfg,thisgfosnum)+'.t'+str(it)+'sm'+str(ism)+'k'+str(kud)+'0.'+PropFormat

def Get2ptCorr(icfg,thisgfosnum,ism,jsm):
    return (CreateCfdir3pt(thisgfosnum)+'twoptsm'+str(ism)+'si'+str(jsm)+
            '/'+CreateCfg(icfg,thisgfosnum)+'.t'+str(it)+'sm'+str(ism)+'k'+str(kud)+'.'+PropFormat+'si'+str(jsm)+'.nucleon.u.2cf')

def Get2ptCorrOutput(icfg,thisgfosnum,ism,jsm):
    return (cfdir+'twoptsm'+str(ism)+'si'+str(jsm)+
            '/'+CreateCfg(icfg,thisgfosnum)+'.t'+str(it)+'sm'+str(ism)+'k'+str(kud)+'.'+PropFormat+'si'+str(jsm)+'.nucleon.u.2cf')

def Get3ptCorr(icfg,thisgfosnum,ism,jsm,tsink,Projector,DS):
    thisREvecDir = REvecFlag+'sm'+str(ism)+REvecFlag+'nD'+str(PoFShifts)+'GMA'+str(Projector)+'t'+str(tsink)+'p'+''.join(map(str,ppvec))+'.'+DS+'/'
    return (CreateCfdir3pt(thisgfosnum)+thisREvecDir+CreateCfg(icfg,thisgfosnum)+'.t'+str(it)+'sm'+str(ism)+REvecFlag+'nD'+str(PoFShifts)+'GMA'+str(Projector)+
            't'+str(tsink)+'p'+''.join(map(str,ppvec))+'.'+DS+'k'+str(kud)+'.'+PropFormat+'.3cf')


