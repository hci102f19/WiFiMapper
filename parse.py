import glob
import json


def lst2dict(lst, key):
    return {k[key]: k for k in lst}


def normalize(lst):
    hotspots = {}

    m = [lst2dict(measurement, 'mac') for measurement in lst]

    for l in m:
        for k, v in l.items():
            if k in hotspots:
                pass
            else:
                hotspots[k] = v

    print(hotspots)
    exit(1)

    return


for file in glob.glob('./output/*.json'):
    data = json.load(open(file, 'r'))

    print(normalize(data))
