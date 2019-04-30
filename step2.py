import glob
import json
from os.path import basename


def get_macs(data):
    macs = []
    [[macs.append(y['mac']) for y in x if y['essid'] == 'AAU-1x'] for x in data]

    return list(set(macs))


for file in glob.glob('./output2/*.json'):
    filenr = basename(file).split('.')[0]
    data = json.load(open(file, 'r'))
    hotspots = {k: None for k in get_macs(data['data'])}

    for scan in data['data']:
        for hotspot in scan:
            if hotspot['mac'] in hotspots:
                if hotspots[hotspot['mac']] is None:
                    hotspots[hotspot['mac']] = {
                        'frequency': hotspot['frequency'],
                        'signal': hotspot['signal'],
                        'mac': hotspot['mac']
                    }
                else:
                    if hotspots[hotspot['mac']]['signal'] > hotspot['signal']:
                        hotspots[hotspot['mac']]['signal'] = hotspot['signal']
    data['data'] = [v for k, v in hotspots.items()]

    json.dump(data, open('./output3/{}.json'.format(filenr), 'w'))
