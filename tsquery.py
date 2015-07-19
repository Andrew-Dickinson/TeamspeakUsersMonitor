import ts3
import json
import pprint

settings = {
    'TS3_IP': 'andrewdickinson.us',
    'TS3_PORT': '10011',
}


def query():
    """
    Query the TeamSpeak3 server for status

    """
    try:
        svr = ts3.TS3Server(settings['TS3_IP'], settings['TS3_PORT'])
        svr.use(1)
    except ts3.ConnectionError:
        return

    response = svr.send_command('serverinfo')
    if response.response['msg'] != 'ok':
        return
    svr_info = response.data[0]

    response = svr.send_command('clientlist')
    if response.response['msg'] != 'ok':
        return
    client_list = response.data

    for client in client_list:
        if client['client_type'] != "0":
            client_list.remove(client)

    avg_ping = svr_info['virtualserver_total_ping']
    bandwidth_down = svr_info['connection_bandwidth_received_last_second_total']
    bandwidth_up = svr_info['connection_bandwidth_sent_last_second_total']

    all_data = {
        'avg_ping': avg_ping,
        'bandwidth_down': bandwidth_down,
        'bandwidth_up': bandwidth_up,
        'connected_users': str(len(client_list)),
        'connected_users_list': client_list
    }

    return all_data