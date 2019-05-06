import json
import socket
from threading import Thread

import math
from flask import Flask, render_template, jsonify

from trilateration_test3 import calc_stuff

app = Flask(__name__)

wifis = {}
mappings = json.load(open('./wifis/GroundFloor.json', 'r'))
mappings = [m for m in mappings if m['mac'] != ""]


def udp_client():
    global wifis
    wifis = json.load(open('./testdata.json', 'r'))
    return
    bytes_to_send = "HELO".encode('utf-8')

    server_address_port = ("192.168.1.101", 20001)

    buffer_size = 4096

    # Create a UDP socket at client side
    udp_client_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    # Send to server using created UDP socket
    udp_client_socket.sendto(bytes_to_send, server_address_port)

    running = True
    while running:
        message, _ = udp_client_socket.recvfrom(buffer_size)

        if message == bytes_to_send:
            continue
        elif message.decode('utf-8') == 'K-BYE':
            running = False
        else:
            wifis = json.loads(message.decode('utf-8'))


def get_distance(frequency, signal):
    exp = (27.55 - (20 * math.log10(frequency)) + abs(int(signal))) / 20.0
    return round(math.pow(10.0, exp), 2)


def mapping(scan):
    for m in mappings:
        if scan['mac'] == m['mac']:
            return {
                'mac': scan['mac'],
                'signal': scan['signal'],
                'color': 'red',
                'lat': m['lat'],
                'lon': m['lon'],
                'dist': get_distance(scan['frequency'], scan['signal'])
            }
    return None


@app.route('/scans')
def scans():
    data = [mapping(t) for t in wifis.get('access_points', []) if mapping(t) is not None]

    # x, y, d = make_circle([(57.01200967, 9.99058806), (57.01212772, 9.99058034)])
    # dist = (EARTH_CIRCUMFERENCE * d / (16 * math.pi))
    # data.append({
    #     'mac': "",
    #     'signal': "",
    #     'color': 'blue',
    #     'lat': x,
    #     'lon': y,
    #     'dist': round(dist, 2)
    # })

    locations = [(d['lat'], d['lon']) for d in data]
    distances = [d['dist'] for d in data]

    k = calc_stuff(locations, distances)

    data.append({
        'mac': "",
        'signal': "",
        'color': 'blue',
        'lat': k[0],
        'lon': k[1],
        'dist': 1
    })

    return jsonify(data)


@app.route('/')
def home():
    return render_template('home_live.html')


if __name__ == '__main__':
    t = Thread(target=udp_client, args=[])
    t.start()

    app.run(
        debug=True,
        host='0.0.0.0'
    )
