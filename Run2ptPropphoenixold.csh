#! /bin/tcsh

#SBATCH -A cssm
#SBATCH -p gpuq
#SBATCH -n 8
#SBATCH --time=20:00:00
#SBATCH --gres=gpu:4
#SBATCH --mem=100GB

module load intel
module load openmpi
module load cuda


set curdir = /home/a1193348/Scripts/FSpython/
cd ${curdir}
set colanewgpu = /home/a1193348/code/cola/OldComp/cuda/
set exe = quarkpropGPU.x


#  If variable icfg is not set, then exit
if (! $?icfg) then
    echo "Error: icfg variable not set."
    exit 1
endif

if (! $?fcfg) then
    echo "fcfg variable not set, setting to icfg"
    set fcfg = ${icfg}
endif

if (! $?gfos) then
    echo "gfos variable not set."
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


if (! $?mach) then
    echo "mach variable not set."
    exit 1
endif


set reportfolder = /data/cssm/jdragos/reports/${mach}/
set reportfile = ${reportfolder}${jobid}.out



    echo "cfg = ${icfg}, ism = ${ism}, mpirun 2 point prop"
    # set reportfile = ${reportdir}"$sm[${ism}]/report"$jobid".out"
    mkdir -p ${reportfile}
    rm ${reportfile} -rf
    echo 'starting '`date`
    # mpirun -np 8 --mca btl ^openib ${colanewgpu}$exe <<EOF > ${reportfile}
    mpirun -np 8 ${colanewgpu}$exe <<EOF > ${reportfile}
${curdir}${jobid}
EOF

    # If previous exec terminated with error, then exit
    if ($? != 0) then
	echo "Error with: ${jobid}"
	echo ""

cat <<EOF >> ${curdir}errlist.2ptprop
${curdir}${jobid}
EOF
	exit 1
    endif
    echo 'finished '`date`

python ${curdir}ReSubmit.py $icfg $fcfg $gfos 'twoptprop' $ism
