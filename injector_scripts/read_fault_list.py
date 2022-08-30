import sys, os
import common


def main():
    args = sys.argv
    fault_list_file = os.path.join(common.APP_DIR, 'fault_list.txt')
    with open(fault_list_file, 'r') as file:
        for line in file.readlines():
            fault = line.split(':')[0]
            if fault == args[1]:
                data = line.split(':')[-1].split(',')
                sm = data[0].split(' ')[-1]
                core = data[1].split(' ')[-1]
                mask = data[2].split(' ')[-1]
                stuckat = data[3].split(' ')[-1]
                instruction = data[4].split(' ')[-1]
                os.environ['SM'] = sm
                os.environ['CORE'] = core
                os.environ['MASK'] = mask
                os.environ['STUCK'] = stuckat
                os.environ['INSTRUCTION'] = instruction
                break


if __name__ == '__main__':
    main()
