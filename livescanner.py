import json
import math
import socket
from threading import Thread

from flask import Flask, render_template, jsonify

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
                'lat': m['lat'],
                'lon': m['lon'],
                'dist': get_distance(scan['frequency'], scan['signal'])
            }
    return None


@app.route('/scans')
def scans():
    data = [mapping(t) for t in wifis.get('access_points', []) if mapping(t) is not None]

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
