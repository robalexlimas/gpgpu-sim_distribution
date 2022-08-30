import os, shutil, sys
from string import Template
import common

"""
This script modified the GPGPUSIM configuration file
and includes the faults injectors params

Arg:
    [enable_faults sm_target core_target mask stuckat type_instruction instrumentation]
example:
    [1 0 0 512 0 310 0]
    -enable_faults 0
    -sm_target 14
    -core_target 1
    -mask 16
    -stuckat 1
    -type_instruction 309
    -instrumentation 1
"""

def main():
    args = sys.argv
    gpgpusim_config_dir = os.path.join(common.GPGPUSIM_DIR, 'configs/tested-cfgs/SM7_TITANV')
    files = os.listdir(gpgpusim_config_dir)
    for file in files:
        source_file = os.path.join(common.GPGPUSIM_DIR, 'configs/tested-cfgs/SM7_TITANV/{}'.format(file))
        destination_file = os.path.join(common.APP_DIR, file)
        shutil.copy(source_file, destination_file)
    config_file = os.path.join(common.APP_DIR, 'gpgpusim.config')
    injector_params = """
# fault injector
-enable_faults $enable
-sm_target $sm
-core_target $core
-mask $mask
-stuckat $stuckat
-type_instruction $inst
-instrumentation $instrumentation
    """
    params = Template(injector_params).substitute(
        enable=args[1], sm=args[2], core=args[3]
        , mask=args[4], stuckat=args[5], inst=args[6], instrumentation=args[7]
    )
    with open(config_file, 'a') as file:
        file.write(params)


if __name__ == '__main__':
    main()
