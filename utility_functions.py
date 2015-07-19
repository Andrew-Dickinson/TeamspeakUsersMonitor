import os
import csv
import datetime
from datetime import timedelta
import dateutil.parser
import shutil

csv_headers = ["Timestamp", "Google Ping", "Router Ping", "Localhost Ping", "CPU use (%)", "Memory use (%)",
               "TS Avg Ping", "TS Bandwidth Down", "TS Bandwidth Up", "TS Users"]


def get_day():
    today = datetime.datetime.now()
    return today.strftime('%Y-%m-%d')


def get_day_shifted():
    today = datetime.datetime.now()
    delta = timedelta(hours=12)
    today = today + delta
    return today.strftime('%Y-%m-%d')


def log(string):
    print string
    f = open('www_dev/log.html', 'r')
    data = f.read()
    f.close()
    f = open('www_dev/log.html', 'w')
    new_data = string + data
    f.write(new_data)
    f.close()


def csv_store(data):
    file_name = 'www_dev/logs/' + get_day() + "_google.csv"
    new_file = not os.path.isfile(file_name)

    f = open(file_name, 'a')
    csv_writer = csv.writer(f, delimiter=',', lineterminator='\n')

    if new_file:
        csv_writer.writerow(csv_headers[0:2])

    if data[1] > 75:
        data[1] = 75

    csv_writer.writerow(data[0:2])

    file_name = 'www_dev/logs/' + get_day() + "_local.csv"
    new_file = not os.path.isfile(file_name)

    f = open(file_name, 'a')
    csv_writer = csv.writer(f, delimiter=',', lineterminator='\n')

    if new_file:
        csv_writer.writerow([csv_headers[0], csv_headers[2], csv_headers[3]])

    csv_writer.writerow([data[0], data[2], data[3]])

    file_name = 'www_dev/logs/' + get_day() + "_sys.csv"
    new_file = not os.path.isfile(file_name)

    f = open(file_name, 'a')
    csv_writer = csv.writer(f, delimiter=',', lineterminator='\n')

    if new_file:
        csv_writer.writerow([csv_headers[0], csv_headers[4], csv_headers[5]])

    csv_writer.writerow([data[0], data[4], data[5]])

    file_name = 'www_dev/logs/' + get_day() + "_ts.csv"
    new_file = not os.path.isfile(file_name)

    f = open(file_name, 'a')
    csv_writer = csv.writer(f, delimiter=',', lineterminator='\n')

    if new_file:
        csv_writer.writerow([csv_headers[0], csv_headers[6], csv_headers[7], csv_headers[8], csv_headers[9]])

    csv_writer.writerow([data[0], data[6], data[7], data[8], data[9]])


def csv_store_ts_presence(data):
    file_name = 'www_dev/logs/' + get_day() + "_ts.csv"
    new_file = not os.path.isfile(file_name)

    f = open(file_name, 'a')
    csv_writer = csv.writer(f, delimiter=',', lineterminator='\n')

    if new_file:
        csv_writer.writerow([csv_headers[0], csv_headers[6], csv_headers[7], csv_headers[8], csv_headers[9]])

    csv_writer.writerow([data[0], data[6], data[7], data[8], data[9]])


def log_new_presence_if_necessary(uid, name):
    file_name = "www_dev/logs/ts_user_dict.csv"
    new_file = not os.path.isfile(file_name)
    found = False
    correct = False
    row_num = -1

    if not new_file:
        f = open(file_name, 'r')
        reader = csv.reader(f, delimiter=',', lineterminator='\n')
        for i, row in enumerate(reader):
            if str(row[0]) == str(uid):
                found = True
                correct = str(name) == str(row[1])
                row_num = i

        f.close()

        if found and correct:
            return False
        else:
            if found and not correct:
                remove_row(file_name, row_num)
                found = False

    if not found:
        f = open(file_name, 'a')
        csv_writer = csv.writer(f, delimiter=',', lineterminator='\n')

        if new_file:
            csv_writer.writerow(["UID", "Name"])

        csv_writer.writerow([uid, name])

        f.close()
        return True


def remove_row(file_name, row_num):
    """Removes a specified row from a csv file"""
    f = open(file_name, 'r')
    reader = csv.reader(f, delimiter=',', lineterminator='\n')
    data = []
    for row in reader:
        data.append(row)
    f.close()

    data.pop(row_num)

    f = open(file_name, 'w')
    writer = csv.writer(f, delimiter=',', lineterminator='\n')

    for row in data:
        writer.writerow(row)

    f.close()


def convert_uid_to_name(uid):
    file_name = "www_dev/logs/ts_user_dict.csv"
    f = open(file_name, 'r')
    reader = csv.reader(f, delimiter=',', lineterminator='\n')
    for row in reader:
        if str(row[0]) == str(uid):
            return row[1]

    return None


def get_time():
    return datetime.datetime.now().replace(microsecond=0)


def log_connection(connection_data):
    log_connection_raw_uid(connection_data)
    file_name = 'www_dev/logs/' + get_day_shifted() + "_ts_connections.csv"
    new_file = not os.path.isfile(file_name)

    f = open(file_name, 'a')
    csv_writer = csv.writer(f, delimiter=',', lineterminator='\n')

    if new_file:
        csv_writer.writerow(["Name", "Time In", "Time Out"])

    csv_writer.writerow([convert_uid_to_name(connection_data[0])] + connection_data[1:])
    f.close()


def log_connection_raw_uid(connection_data):
    file_name = 'www_dev/logs/ts_connections_raw_uid.csv'
    new_file = not os.path.isfile(file_name)

    f = open(file_name, 'a')
    csv_writer = csv.writer(f, delimiter=',', lineterminator='\n')

    if new_file:
        csv_writer.writerow(["UID", "Time In", "Time Out"])

    csv_writer.writerow(connection_data)
    f.close()


def log_current_users(user_data_list):
    log_current_users_raw_uid(user_data_list)
    file_name = 'www_dev/logs/current_ts_connections.csv'

    f = open(file_name, 'w')
    csv_writer = csv.writer(f, delimiter=',', lineterminator='\n')
    csv_writer.writerow(["Name", "Time In", "Time Out"])

    for connection_data in user_data_list:
        csv_writer.writerow([convert_uid_to_name(connection_data[0])] + connection_data[1:])

    if len(user_data_list) == 0:
        csv_writer.writerow(["null", get_time(), get_time()])

    f.close()


def log_current_users_raw_uid(user_data_list):
    file_name = 'www_dev/logs/current_ts_connections_raw_uid.csv'

    f = open(file_name, 'w')
    csv_writer = csv.writer(f, delimiter=',', lineterminator='\n')
    csv_writer.writerow(["UID", "Time In", "Time Out"])

    for connection_data in user_data_list:
        csv_writer.writerow(connection_data)

    f.close()


def merge_ts_connection_files():
    merge_ts_connection_files_raw_uid()
    cur_file_name = 'www_dev/logs/current_ts_connections.csv'
    cur_file = open(cur_file_name, 'r')
    cur_reader = csv.reader(cur_file, delimiter=',', lineterminator='\n')

    past_file_name = 'www_dev/logs/' + get_day_shifted() + "_ts_connections.csv"
    new_file = not os.path.isfile(past_file_name)
    if not new_file:
        past_file = open(past_file_name, 'r')
        past_reader = csv.reader(past_file, delimiter=',', lineterminator='\n')

    merge_file_name = 'www_dev/logs/merged_ts_connections.csv'
    merge_file = open(merge_file_name, 'w')
    merge_writer = csv.writer(merge_file, delimiter=',', lineterminator='\n')

    for i, row in enumerate(cur_reader):
        merge_writer.writerow(row)

    if not new_file:
        for i, row in enumerate(past_reader):
            if i != 0:
                merge_writer.writerow(row)

        past_file.close()

    merge_file.close()
    cur_file.close()


def merge_ts_connection_files_raw_uid():
    cur_file_name = 'www_dev/logs/current_ts_connections_raw_uid.csv'
    cur_file = open(cur_file_name, 'r')
    cur_reader = csv.reader(cur_file, delimiter=',', lineterminator='\n')

    past_file_name = 'www_dev/logs/ts_connections_raw_uid.csv'
    new_file = not os.path.isfile(past_file_name)
    if not new_file:
        past_file = open(past_file_name, 'r')
        past_reader = csv.reader(past_file, delimiter=',', lineterminator='\n')

    merge_file_name = 'www_dev/logs/merged_ts_connections_raw_uid.csv'
    merge_file = open(merge_file_name, 'w')
    merge_writer = csv.writer(merge_file, delimiter=',', lineterminator='\n')

    if not new_file:
        for i, row in enumerate(past_reader):
            if i != 0:
                merge_writer.writerow(row)

        past_file.close()

    for i, row in enumerate(cur_reader):
            merge_writer.writerow(row)

    merge_file.close()
    cur_file.close()


def update_user_specific_logs():
    merge_file_name = 'www_dev/logs/merged_ts_connections_raw_uid.csv'
    merge_file = open(merge_file_name, 'r')
    merge_reader = csv.reader(merge_file, delimiter=',', lineterminator='\n')

    data_array = []
    for row in merge_reader:
        data_array.append(row)

    data_array.pop(0)
    merge_file.close()

    uid_list = []
    for row in data_array:
        if not row[0] in uid_list:
            uid_list.append(row[0])

    for uid in uid_list:
        client_connections = []
        for row in data_array:
            if row[0] == uid:
                client_connections.append(row)

        for connection in client_connections:
            connection_time = dateutil.parser.parse(connection[1])
            delta = timedelta(hours=12)
            connection_time = connection_time - delta
            connection[0] = connection_time.strftime('%Y-%m-%d')

        directory = 'www_dev/logs/' + str(uid) + '/'
        if not os.path.exists(directory):
            os.makedirs(directory)

        html_path_final = 'www_dev/logs/' + str(uid) + '/individual_connections.html'
        html_path_original = 'individual_connections.html'
        if not os.path.exists(html_path_final):
            shutil.copyfile(html_path_original, html_path_final)

        log_file_name = directory + str(uid) + "_connections.csv"
        log_file = open(log_file_name, 'w')
        log_writer = csv.writer(log_file, delimiter=',', lineterminator='\n')
        log_writer.writerow(["Date", "Time In", "Time Out"])

        for row in client_connections:
            log_writer.writerow(row)

        log_file.close()




