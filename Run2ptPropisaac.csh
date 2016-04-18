#! /bin/tcsh

#SBATCH -A a1193348
#SBATCH -p batch
#SBATCH -n 16
#SBATCH --time=20:00:00
#SBATCH --gres=gpu:4
#SBATCH --mem=55GB

module load openmpi-uofa-intel
module load cuda/6.0
 
set curdir = /home/a1193348/Scripts/FSpython/
cd ${curdir}
set colanewgpu = /home/a1193348/code/cola/jfsmNew_w2/cuda/
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


set reportfolder = /data/jdragos/reports/${mach}/
set reportfile = ${reportfolder}${jobid}.out



    echo "cfg = ${icfg}, ism = ${ism}, mpirun 2 point prop"
    # set reportfile = ${reportdir}"$sm[${ism}]/report"$jobid".out"
    mkdir -p ${reportfile}
    rm ${reportfile} -rf
    echo 'starting '`date`
    # mpirun -np 16 --mca btl ^openib ${colanewgpu}$exe <<EOF > ${reportfile}
    mpirun -np 16 ${colanewgpu}$exe <<EOF > ${reportfile}
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
