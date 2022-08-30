import os, random
import common


def read_instructions():
    result_file = os.path.join(common.APP_DIR, 'out.txt')
    instructions = dict()
    with open(result_file, 'r') as file:
        lines = file.readlines()
    for line in lines:
        if 'Type instruction ->' in line:
            inst = int(line.split('Type instruction ->')[-1])
            keys = instructions.keys()
            if inst in keys:
                instructions[inst] = instructions[inst] + 1
            else:
                instructions[inst] = 0
    return [str(inst) for inst in instructions.keys()]


def generate_fault_list(instructions):
    faults = []
    for fault in range(int(common.TOTAL_FAULTS)):
        mask = random.randint(0, 31)
        faults.append(
            '{}: SM {}, CORE {}, MASK {}, STUCKAT {}, INSTRUCTION {}\n'
            .format(
                fault, common.SM_TARGET, common.CORE_TARGET, 2 ** mask, common.STUCKAT, random.choice(instructions)
            )
        )
    return faults


def create_faults_file(faults):
    faults_file = os.path.join(common.APP_DIR, 'fault_list.txt')
    with open(faults_file, 'w') as file:
        for fault in faults:
            file.write('{}'.format(fault))


def create_golden_out():
    result_file = os.path.join(common.APP_DIR, 'out.txt')
    golden_out = []
    start, end = False, False
    with open(result_file, 'r') as file:
        lines = file.readlines()
    for line in lines:
        if start and not end:
            golden_out.append(line)
        if 'RESULTS START HERE' in line:
            start = True
        if 'RESULTS END HERE' in line:
            end = True
    golden_file = os.path.join(common.APP_DIR, 'golden.txt')
    with open(golden_file, 'w') as file:
        for line in golden_out:
            file.write(line)


def main():
    instructions = read_instructions()
    faults = generate_fault_list(instructions)
    create_faults_file(faults)
    create_golden_out()


if __name__ == '__main__':
    main()
