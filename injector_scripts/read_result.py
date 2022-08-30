import os
import common


def create_stdout():
    result_file = os.path.join(common.APP_DIR, 'out.txt')
    result_path = os.path.join(common.APP_DIR, 'results')
    if not os.path.isdir(result_path):
        os.mkdir(result_path)
    golden_out = []
    start, end = False, False
    with open(result_file, 'r') as file:
        lines = file.readlines()
    for line in lines:
        if 'RESULTS END HERE' in line:
            end = True
        if start and not end:
            golden_out.append(line)
        if 'RESULTS START HERE' in line:
            start = True
    stdout_file = os.path.join(
        result_path,
        'stdout_{}.txt'.format(os.getenv('TOTAL_FAULTS'))
    )
    with open(stdout_file, 'w+') as file:
        for line in golden_out:
            file.write(line)


def main():
    create_stdout()


if __name__ == '__main__':
    main()
