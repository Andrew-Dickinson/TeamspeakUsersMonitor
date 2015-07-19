import ping
import math
import socket
import datetime
import time
import re
import psutil
import tsquery
from utility_functions import csv_store, log, log_new_presence_if_necessary, \
    get_time, log_connection, convert_uid_to_name, log_current_users, merge_ts_connection_files,\
    update_user_specific_logs

past_client_list = []
timeline_stack = []


def run():
    global past_client_list
    global timeline_stack
    data = tsquery.query()
    client_ids = []
    for client in data['connected_users_list']:
        regex_string = "Unknown from \d*.\d*.\d*.\d*:.\d*"
        name = client['client_nickname']
        real = None == re.search(regex_string, name)
        if real:
            client_ids.append(client['client_database_id'])
            log_new_presence_if_necessary(client['client_database_id'], client['client_nickname'])

    add_list = []
    for client in client_ids:
        if not client in past_client_list:
            add_list.append(client)

    drop_list = []
    for client in past_client_list:
        if not client in client_ids:
            drop_list.append(client)

    past_client_list = client_ids

    for client in add_list:
        timeline_stack.append([client, get_time(), None])
        print convert_uid_to_name(client) + " connected!"

    for client in drop_list:
        print convert_uid_to_name(client) + " disconnected!"
        for line in timeline_stack:
            if line[0] == client:
                line[2] = get_time()
                log_connection(line)
                timeline_stack.remove(line)

    # Log the current users in a different system under the same format
    cur_stack = []
    for client in client_ids:
        for line in timeline_stack:
            new_line = line[:]
            if client == line[0]:
                new_line[2] = get_time()
                cur_stack.append(new_line)
    log_current_users(cur_stack)

    merge_ts_connection_files()
    # update_user_specific_logs()


while True:
    run()
    time.sleep(10)