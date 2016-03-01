#!/usr/bin/env python

import os
from RunParams import *
from shutil import copyfile,move,rmtree
import subprocess
from FilenameFuns import *

def GetGaugeField(icfg,thisgfosnum):
    limefile = CreateLimeCfg(icfg,thisgfosnum)
    limepath = rdsigfdir+limefile
    if os.path.isfile(limepath):
        if os.path.isfile(gfdir+CreateCfg(icfg,thisgfosnum)):
            print gfdir+CreateCfg(icfg,thisgfosnum) , ' Already present'
        else:
            print 'Copying Gf from: '+limepath
            copyfile(limepath,gfdir+limefile)
            subprocess.call([limedir+"lime_unpack",gfdir+limefile])
            move(gfdir+limefile+'.contents/msg01.rec02.ildg-binary-data',gfdir+CreateCfg(icfg,thisgfosnum))
            rmtree(gfdir+limefile+'.contents/')
            os.remove(gfdir+limefile)
            print 'Copying complete'
    else:
        print 'Warning: ' , limepath , ' Does not exist'

def RemoveGaugeField(icfg,thisgfosnum):
    gffile = gfdir+CreateCfg(icfg,thisgfosnum)
    if os.path.isfile(gffile):
        print 'Deleting: ' , gffile
        os.remove(gffile)
    else:
        print gffile , ' not present'


def RemoveProp(icfg,thisgfosnum,thisismlist):
    for ism in thisismlist:
        thisfile = Get2ptProp(icfg,thisgfosnum,ism)
        if os.path.isfile(thisfile):
            print 'Removing: ',thisfile
            os.remove(thisfile)
        else:
            print thisfile,' not present'


def Move2ptCorr(icfg,thisgfosnum,thisismlist,thisjsmlist):
    for ism in thisismlist:
        for jsm in thisjsmlist:
            thisoutfile = Get2ptCorrOutput(icfg,thisgfosnum,ism,jsm)
            thisfile = Get2ptCorr(icfg,thisgfosnum,ism,jsm)
            if os.path.isfile(thisoutfile):
                move(thisoutfile,thisfile)

def Check2ptProp(icfg,thisgfosnum,thisismlist):
    Present = True
    for ism in thisismlist:
        thisfile = Get2ptProp(icfg,thisgfosnum,ism)
        if not os.path.isfile(thisfile): 
            Present = False
    return Present

def Check2ptCorr(icfg,thisgfosnum,thisismlist,thisjsmlist):
    Present = True
    for ism in thisismlist:
        for jsm in thisjsmlist:
            thisfile = Get2ptCorr(icfg,thisgfosnum,ism,jsm)
            if not os.path.isfile(thisfile): 
                Present = False
    return Present

def Check3ptCorr(icfg,thisgfosnum,thisismlist,tsinklist,Projectorlist,DSlist):
    Present = True
    for ism in thisismlist:
        for tsink in tsinklist:
            for Projector in Projectorlist:
                for DS in DSlist:
                    thisfile = Get3ptCorr(icfg,thisgfosnum,ism,tsink,Projector,DS)
                    if not os.path.isfile(thisfile): 
                        Present = False
    return Present
