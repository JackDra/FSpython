#!/usr/bin/env python

import os
import errno


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise

thismachine = 'phoenix'

#james prop gf source index parameter
SRCX = [ 0, 16,  0, 16,  0,  0, 16, 16, 16, 16 ]#0  0  0 16  0 16 )
SRCY = [ 0, 16,  0,  0, 16, 16,  0,  0, 16, 16 ]#0 16 16  0  0 16 )
SRCZ = [ 0, 16,  0, 16,  0, 16,  0, 16,  0, 16 ]#16  0 16  0 16  0 )
SRCT = [ 0,  4, 32, 60, 24, 48, 12, 28, 20, 36 ]#40 56 16 44  8 52 )

#Taken from /home/accounts/jdragos/scripts/PythonAnalysis/REvecSave/k12090/PoF1to16dt2LREM.txt
RVec = [ 76.3260613436,  -161.5448230802, 264086.1917824702, -321.4016231030, 4390.5310121576, -893677.8525444396 ]

FortFileFlag = 'params'

# Testing, should be same as tsink sm128
# RVec = ( 0.0 0.0 0.0 0.0 0.0 1.0 )

##n.b. PoFShifts = 1 means 1 tsink value (so no PoF)
PoFShifts = 1

REvecFlag = 'REPoFto16dt2'
# REvecFlag = 'REPoFTest'
####COLA PARAMETERS
# lattice params, note that cube so no need for ny/nz
nx = 32
nt = 64

# Propagator Params
it = 16 # creation parameters
ix = 1 #put at ix,ix,ix
GrpFormat = 'ildg-sp' #group format
PropFormat = 'ifms' #propagator format
ParrIO = 'F' # parrallel io
# kud = 12104 # kappa (quark hopping) params
# ks = 12062
kud = 12090 # kappa (quark hopping) params
ks = 12090
SourceType = 3 ## regular source smeared propagator
Prec = '1.0d-5'
# Projector = 4
GammaRep = 'sakurai'
ProjectorList = [4,3]
DSList = ['doub','sing']
WriteProp = 'T'

# SST Propagator Parameters
# it_sst = '32 35 38' ## ahnialation parameters (momenta)
it_sst = [26, 27, 28, 29, 30] ## ahnialation parameters (momenta)
TSstart = 26
ppvec = [0,0,0]
qmin = 0
qmax = 9
sstSourceType = 5 ## SST calculation = 5
FSSourceType = 6 #My modified version = 6
CMFSSourceType = 7 #My modified version for correlation matrix pre inversion = 7
NDer = 1

# Smearing Parameters
alpha = 0.7
StoutLink = 'T'
alphaStout = 0.1
gfsweeps = 4
smu0 = 1.0
smvalues = [32, 64, 128, 'V0']
ismlist = smvalues[:-1]
jsmlist = smvalues[:-1]

# twoptinterps = 'nucleon nucleon2 nucleon_nucleon2 nucleon2_nucleon'
twoptinterps = 'nucleon'

# REvecFlag = 'REvec'
##PUT RESum##to####

# Boundary Conditions (clover)
bx = 1.0
by = 1.0
bz = 1.0
bt = 0.0
u0 = 1.0
csw = 2.65
rho = 0.1
nstout = 1

####gencf parameters
MCTFormat = 'gencf'
nkappa = 1
kappa_s = 0
Ustar = 'F'
gamma_rep = GammaRep
parallelIO = 'f'
sinksmear = 'T'
# pmin=0=pmax is fine too, but using pmax=2 may break(?)
pmin = 0
pmax = 9
iq = 0
jmin = 0
jmax = 0
ijmu = 0



# Configuration data
limename = 'qcdsf'
ensemble = 'b5p50kp'+str(kud)+'0kp'+str(ks)+'0'

#### configuration/file parameters
basedir = '/home/a1193348/'
scratchdir = '/data/cssm/jdragos/'
scriptdir = basedir+'Scripts/FSpython/'
datadir = scratchdir
FortFolderPref = 'FortFiles'
FortFolder = scriptdir+FortFolderPref+'/'
homedir = datadir+'/run-gencf/PACS-CS/'
reportdir = datadir+'/run-gencf/'+thismachine+'/PACS-CS/'
gfdir = scratchdir+'/gaugefields/'+ensemble+'/'
# rdsigfdir = '/data/jzanotti/confs/32x64/b5p50kp121040kp120620/'
# rdsigfdir = scratchdir+'/gaugefields/limes/
# ##for heavier kappa
rdsigfdir = scratchdir+'/gaugefields/qcdsf.655/'
# gfdir = '/rdsi/PACS-CS/ensemble+'/'
qpdir = scratchdir+'/qprops/k'+str(kud)+'/'+PropFormat+'/'
cfdir = scratchdir+'/cfun/2ndk'+str(kud)+'/'
debugdir = scratchdir+'/debug/2ndk'+str(kud)+'/'
fstwoptdir = scratchdir+'/fstwoptdir/2ndk'+str(kud)+'/'
G2resdir = scratchdir+'/G2resdir/k'+str(kud)+'/'
G2ffresdir = scratchdir+'/G2ffresdir/k'+str(kud)+'/'
tempdir = '/tmp/'
filelists = datadir+'/'
codedir = basedir+'/code'
colanewgpu = codedir+'/cola/jfsmNew_w2/cuda/'
colanewmod = codedir+'/cola/jfsmNew_w2/bin/'
limedir = codedir+'/ildg/lroot/bin/'
gencfeff = codedir+'/gencf/bin/'
gencfnew = codedir+'/newgencf/trunk/bin/'

# gfnum = `head -n $icfg ${filelists}${cfglist} | tail -n 1`
# cfg = ensemble+str(gfnum)
# limecfg = limename+str(gfnum)+'.lime'

# cfglist = "cfglist"+thismachine+str(gfosnum)
# cfdir3pt = scratchdir+'/cfun/2ndk'+str(kud)+'/source'+str(gfosnum)+'/'

def CreateCfgFilename(gfosnum):
    return "cfglist"+thismachine+str(gfosnum)

def CreateCfdir3pt(gfosnum):
    return scratchdir+'/cfun/2ndk'+str(kud)+'/source'+str(gfosnum)+'/'

def CreateGFnum(icfg,gfosnum):
    with open(filelists+CreateCfgFilename(gfosnum),'r') as f:
        thisgfnum = f.readlines()[icfg].replace('\n','')
    return thisgfnum

def CreateCfg(icfg,gfosnum):
    return ensemble+CreateGFnum(icfg,gfosnum)

def CreateLimeCfg(icfg,gfosnum):
    return limename+CreateGFnum(icfg,gfosnum)+'.lime'



##Make directories

mkdir_p(datadir)
mkdir_p(homedir)
mkdir_p(FortFolder)
mkdir_p(reportdir)
mkdir_p(gfdir)
mkdir_p(qpdir)
mkdir_p(cfdir)
# mkdir_p(cfdir3pt)
mkdir_p(G2resdir)
mkdir_p(G2ffresdir)
# mkdir_p(tempdir)
mkdir_p(debugdir)
mkdir_p(fstwoptdir)

