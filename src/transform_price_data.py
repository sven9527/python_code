import csv, os
import mysql.connector


result_file_path = "output/ts_test.csv"
result_file_path_2 = "output/ts_ts_with_price.csv"


def get_price(data):
    conn = mysql.connector.connect(host="rm-bp1i8kq0m43thfr9wso.mysql.rds.aliyuncs.com",
                                   user="walmart_dev", passwd="LHbq3KYH555S", db="walmart_data", port=3306)
    cursor = conn.cursor()
    try:

        for item in data:
            upc = os.path.splitext(item[1])[0].split('_')[-1]
            sql = "select price from upc_price where upc = '{}'".format(upc)
            cursor.execute(sql)
            values = cursor.fetchall()
            item.append(upc)
        return data
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

def write_price_2_csv(data):
    with open(result_file_path_2, 'a') as f:
        csv_writer = csv.writer(f)
        for item in data:
            csv_writer.writerow(item)


def read_ts_upc():
    upc_list = []
    data = []
    with open(result_file_path) as f:
        csv_reader = csv.reader(f)
        for item in csv_reader:
            success = int(item[0])
            ticket_switch = -1 if item[3] == '' else int(item[3])
            if success == 1 and ticket_switch == 1:
                data.append(item)
                upc = os.path.splitext(item[1])[0].split('_')[-1]
                upc_list.append(upc)
    data = get_price(data)
    write_price_2_csv(data)


def get_price_by_upc(upc):
    conn = mysql.connector.connect(host="rm-bp1i8kq0m43thfr9wso.mysql.rds.aliyuncs.com",
                                   user="walmart_dev", passwd="LHbq3KYH555S", db="walmart_data", port=3306)
    cursor = conn.cursor()
    try:
        sql = "select price from upc_price where upc = '{}'".format(upc)
        cursor.execute(sql)
        values = cursor.fetchall()
        print(values)
    except Exception:
        pass
    finally:
        cursor.close()
        conn.close()


def transform_price_2_wlm_db():
    # total_data_num = 1697904
    total_data_num = 100
    step = 5
    conn = mysql.connector.connect(host="rm-j6c7v3st3d6846b4w7o.mysql.rds.aliyuncs.com",
                                   user="walmart_dev", passwd="123QWEasd", db="walmart_data", port=3306)
    cursor = conn.cursor()

    try:
        for i in range(0,total_data_num,step):
            sql = "SELECT upc FROM walmart_product_with_volume ORDER BY id LIMIT {0},{1}".format(i, step)
            cursor.execute(sql)
            values = cursor.fetchall()
            print(values)
    except Exception as e:
        pass
    finally:
        cursor.close()
        conn.close()




if __name__ == '__main__':
    # read_ts_upc()
    transform_price_2_wlm_db()