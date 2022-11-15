import filecmp, json, os
import common


def read_results():
    app_dir = common.APP_DIR
    total_faults = common.TOTAL_FAULTS
    results_dir = os.path.join(app_dir, 'results')
    result_path = os.path.join(app_dir, 'results.json')
    golden_file = os.path.join(app_dir, 'golden.txt')
    results = {
        'equals': [],
        'diff': [],
        'safe': {
            'percentage': 0,
            'total': 0
        },
        'critical': {
            'percentage': 0,
            'total': 0
        },
        'due': {
            'percentage': 0,
            'total': 0
        }
    }
    files = os.listdir(results_dir)
    for file in files:
        file_path = os.path.join(results_dir, file)
        diff = not filecmp.cmp(file_path, golden_file)
        if diff:
            results['diff'].append(file)
        else:
            results['equals'].append(file)
    results['safe']['total'] = len(results['equals'])
    results['safe']['percentage'] = (len(results['equals']) / int(total_faults)) * 100
    results['critical']['total'] = len(results['diff'])
    results['critical']['percentage'] = (len(results['diff']) / int(total_faults)) * 100
    results['due']['total'] = int(total_faults) - len(results['equals']) - len(results['diff'])
    results['due']['percentage'] = (results['due']['total'] / int(total_faults)) * 100
    with open(result_path, 'w') as f:
        json.dump(results, f)


def main():
    read_results()


if __name__ == '__main__':
    main()
