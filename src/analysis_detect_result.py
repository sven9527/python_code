import csv, json

result_file_path = "output/2018-12-07 10:24:40_ts_result_legacy.csv"

result = {
    'total_num': 0,
    'success_num': 0,
    'success_rat': 0,
    'fail_num': 0,
    'fail_rat': 0,
    'ticket_switch_num': 0,
    'ticket_switch_rat': 0,
    'errors': {},
    'unsupported_upc': []
}


def analysis(result_file_path):
    with open(result_file_path) as f:
        csv_reader = csv.reader(f)
        for item in csv_reader:
            result['total_num'] += 1
            try:
                if int(item[0]) == 1:
                    result['success_num'] += 1
                    if int(item[3]) == 1:
                        result['ticket_switch_num'] += 1
                else:
                    result['fail_num'] += 1
                    error_info = json.loads(item[-1])
                    if error_info['error_code'] in result['errors']:
                        result['errors'][error_info['error_code']] += 1
                    else:
                        result['errors'][error_info['error_code']] = 1
                        result['unsupported_upc'].append(item[2])
            except Exception as e:
                print(e)


def calculate():
    result['success_rat'] = result['success_num'] / result['total_num']
    result['fail_num'] = result['fail_num'] / result['total_num']
    result['ticket_switch_rat'] = result['ticket_switch_num'] / result['success_num']


if __name__ == '__main__':
    analysis(result_file_path)
    calculate()
    print(result)
