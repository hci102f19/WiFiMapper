import glob
import json
import math

from flask import Flask, jsonify, render_template

app = Flask(__name__)


def get_distance(frequency, signal):
    exp = (27.55 - (20 * math.log10(frequency)) + abs(int(signal))) / 20.0
    return round(math.pow(10.0, exp), 2)


@app.route('/scans')
def scans():
    scans = []
    for file in glob.glob('./output3/*.json'):
        data = json.load(open(file, 'r'))
        for i in range(len(data['data'])):
            el = data['data'][i]
            data['data'][i]['distance'] = get_distance(el['frequency'], el['signal'])
        scans.append(data)
    return jsonify(scans)


@app.route('/')
def home():
    return render_template('home.html')


if __name__ == '__main__':
    app.run(
        debug=True,
        host='0.0.0.0'
    )