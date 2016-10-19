#! /bin/tcsh
#SBATCH -p batch
#SBATCH -n 8
#SBATCH --time=5:00:00
#SBATCH --gres=gpu:4
#SBATCH --mem=48GB
#SBATCH --qos=gxl

module load intel/2015c
module load OpenMPI/1.8.8-iccifort-2015.3.187
module load CUDA/7.0.28

set curdir = /home/a1193348/Scripts/FSpython/
cd ${curdir}
set colanewgpu = /home/a1193348/code/cola/jfsmNew_w2/cuda/
# set colanewgpu = /home/a1193348/code/cola/cola/cuda/
set exe = quarkpropfstrGPU.x


#  If variable icfg is not set, then exit
if (! $?icfg) then
    echo "Error: icfg variable not set."
    exit 1
endif

if (! $?ism) then
    echo "ism variable not set."
    exit 1
endif

if (! $?jobid) then
    echo "jobid variable not set."
    exit 1
endif

if (! $?fcfg) then
    echo "fcfg variable not set, setting to icfg"
    set fcfg = ${icfg}
endif

if (! $?mach) then
    echo "mach variable not set."
    exit 1
endif

if (! $?tsink) then
    echo "tsink variable not set."
    exit 1
endif

if (! $?Projector) then
    echo "Projector variable not set."
    exit 1
endif

if (! $?DS) then
    echo "DS variable not set."
    exit 1
endif


set reportfolder = /data/cssm/jdragos/reports/${mach}/
set reportfile = ${reportfolder}${jobid}.out

    mkdir -p ${reportfile}
    rm ${reportfile} -rf
    echo "mpirun 3 point GMA${Projector} ${DS}, tsink = ${tsink} ism = ${ism} "
    echo 'starting '`date`
    mpirun -np 8 ${colanewgpu}$exe --solver='CGNE+S' <<EOF >> ${reportfile}
${curdir}${jobid}
EOF

    # If previous exec terminated with error, then exit
    if ($? != 0) then
	echo "Error with: ${jobid}"
	echo ""

	python ${curdir}ReSubmit.py $icfg $fcfg $gfos 'threeptcorr' $ism 'Failed' $tsink $Projector $DS
	cat <<EOF >> ${curdir}errlist.3ptcorr
	${jobid}
	EOF
	exit 1
    endif
    echo 'finished '`date`

python ${curdir}ReSubmit.py $icfg $fcfg $gfos 'threeptcorr' $ism 'Complete' $tsink $Projector $DS
