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
export TOTAL_FAULTS=2
export SM_TARGET=0
export CORE_TARGET=0
export STUCKAT=0

# REMOVE THE PREVIOUS SIMULATIONS
rm -r $APP_DIR/checkpoint_files/
rm $APP_DIR/_app_cuda_version_*
rm $APP_DIR/_cuobjdump_list_ptx_*
rm $APP_DIR/gpgpu_inst_stats.txt 
rm $APP_DIR/$APP_NAME.1.sm_70.ptx*
rm $APP_DIR/out.txt

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
python3 $GPGPUSIM_DIR/injector_scripts/fault_list.py
###############################################################################

###############################################################################
# RUN THE DIVERSE FAULTS
while [ $TOTAL_FAULTS -ge 0 ]
do 
    ((TOTAL_FAULTS--))
    python3 $GPGPUSIM_DIR/injector_scripts/read_fault_list.py $TOTAL_FAULTS
    echo "Fault: $TOTAL_FAULTS, SM Target $SM, CORE target $CORE, MASK $MASK, STUCKAT $STUCK, INSTRUCTION $INSTRUCTION"
    # enable_faults sm_target core_target mask stuckat type_instruction instrumentation
    python3 $GPGPUSIM_DIR/injector_scripts/load_params_sim.py 1 0 0 0 0 310 0
    #python3 $GPGPUSIM_DIR/injector_scripts/load_params_sim.py 1 $SM $CORE $MASK $STUCK $INSTRUCTION 0
    ./$APP_NAME > $APP_DIR/out.txt
    python3 $GPGPUSIM_DIR/injector_scripts/read_result.py
done
