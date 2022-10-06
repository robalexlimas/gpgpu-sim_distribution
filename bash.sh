#!/bin/bash
#
# Robert Alexander Limas Sierra
#

# stop after first error 
set -e 

###############################################################################
find . -name "*.sh" | xargs chmod +x
###############################################################################

# ENVIRONMENT VARIABLES
export GPGPUSIM_DIR=/home/robert/Documents/gpgpu-sim_distribution
export APP_DIR=/home/robert/Documents/GPGPU-SIM-Test/Fake
export APP_NAME=mul

# VARIABLES
export TOTAL_FAULTS=100
export FAULT=0
export SM_TARGET=0
export CORE_TARGET=0
export STUCKAT=0

# REMOVE THE PREVIOUS SIMULATIONS
rm -r $APP_DIR/checkpoint_files/
rm $APP_DIR/_app_cuda_version_*
rm $APP_DIR/_cuobjdump_list_ptx_*
rm $APP_DIR/gpgpu_inst_stats.txt 
rm $APP_DIR/$APP_NAME.1.sm_70.ptx*
rm $APP_DIR/times.txt
rm -r $APP_DIR/outs/
rm -r $APP_DIR/results/

mkdir $APP_DIR/results
mkdir $APP_DIR/outs

###############################################################################
# GO TO GPGPUSIM DIR
cd $GPGPUSIM_DIR
# ENABLE THE SIMULATOR IN DEGUB MODE
source setup_environment debug
# GO TO APP DIR
cd $APP_DIR
# COMPILE THE APP
nvcc $APP_NAME.cu -o $APP_NAME -lcudart -gencode arch=compute_70,code=compute_70
# CONFIGURE THE APP
ldd $APP_NAME

###############################################################################
# OBTAIN THE GOLDEN OUT AND CREATE THE FAULT LIST
# enable_faults sm_target core_target mask stuckat type_instruction instrumentation
python3 $GPGPUSIM_DIR/injector_scripts/load_params_sim.py 0 0 0 0 0 0 1
./$APP_NAME > $APP_DIR/out.txt
#python3 $GPGPUSIM_DIR/injector_scripts/fault_list.py
mv $APP_DIR/out.txt $APP_DIR/outs/golden_out.txt
###############################################################################

###############################################################################
# RUN THE DIVERSE FAULTS
TIMES=''
while read -a line
do
    start_ns=`date +%s%N`
    FAULT=${line[0]}
    SM=${line[2]}
    CORE=${line[4]}
    MASK=${line[6]}
    STUCK=${line[8]}
    INSTRUCTION=${line[10]}
    echo "Fault: $FAULT, SM Target $SM CORE target $CORE MASK $MASK STUCKAT $STUCK INSTRUCTION $INSTRUCTION"
    # enable_faults sm_target core_target mask stuckat type_instruction instrumentation
    python3 $GPGPUSIM_DIR/injector_scripts/load_params_sim.py 1 $SM $CORE $MASK $STUCK $INSTRUCTION 0
    ./$APP_NAME > $APP_DIR/out.txt
    python3 $GPGPUSIM_DIR/injector_scripts/read_result.py
    mv $APP_DIR/out.txt $APP_DIR/outs/out_$FAULT.txt
    end_ns=`date +%s%N`
    let total_ns=$end_ns-$start_ns
    echo "Time: $total_ns- nanosegudos"
    echo "$total_ns" >> $APP_DIR/times.txt
done < $APP_DIR/fault_list.txt
ls $APP_DIR/results/ | wc -l
ls -lah $APP_DIR/outs/ |cut -d ' ' -f 5 > $APP_DIR/outs/sizes.txt
