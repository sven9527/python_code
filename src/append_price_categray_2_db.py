import math
import csv

csv_path = 'source_data/upc-db-with-price-2018-12-15.csv'
output_path = 'source_data/department_id_and_name.csv'
output_append_data_path = 'source_data/output_append_data.csv'

def load_data_from_csv():
    department_info = set()
    with open(csv_path, 'r') as f:
        csv_reader = csv.reader(f)
        for line in csv_reader:
            fields = line[0].split('|')
            tmp = (fields[1], fields[2])
            department_info.add(tmp)
    return department_info


def save_department_info(department_info):
    def take_one(ele):
        return int(ele[0])
    department_info = list(department_info)
    department_info.sort(key=take_one)
    with open(output_path, 'w') as f:
        csv_writer = csv.writer(f)
        for l in department_info:
            csv_writer.writerow(l)


def load_append_info():
    append_info = []
    with open(csv_path, 'r') as f:
        csv_reader = csv.reader(f)
        for line in csv_reader:
            fields = line[0].split('|')
            price = int(fields[-5])/100
            append_info.append([math.ceil(float(fields[3])), int(fields[1]), fields[2], price, float(fields[-4]), float(fields[-3]), float(fields[-2])])

    with open(output_append_data_path, 'w') as f:
        csv_writer = csv.writer(f)
        for line in append_info:
            csv_writer.writerow(line)

if __name__ == '__main__':
    load_append_info()
