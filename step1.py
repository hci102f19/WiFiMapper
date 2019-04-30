import glob
import json
from os.path import basename

mappers = {
    '1': {'lat': 57.01200394356648, 'lon': 9.990482823738148},
    '2': {'lat': 57.012087694574745, 'lon': 9.990484934515052},
    '3': {'lat': 57.012130529832106, 'lon': 9.990483911538718},
    '4': {'lat': 57.012084930430674, 'lon': 9.990624303000573},
    '5': {'lat': 57.01208275459077, 'lon': 9.99076464833081},
    '6': {'lat': 57.01203931592761, 'lon': 9.990765914737608},
    '7': {'lat': 57.0119939314569, 'lon': 9.990758624084378},
    '8': {'lat': 57.01194708927545, 'lon': 9.99076703452306},
    '9': {'lat': 57.011907695732546, 'lon': 9.99076320125323},
    '10': {'lat': 57.01191115724374, 'lon': 9.99066078700173},
    '11': {'lat': 57.01190898799123, 'lon': 9.99053802566209},
}

for file in glob.glob('./output/*.json'):
    filenr = basename(file).split('.')[0]
    data = json.load(open(file, 'r'))

    new_dict = mappers[filenr]
    new_dict['data'] = data

    json.dump(new_dict, open('./output2/{}.json'.format(filenr), 'w'))
