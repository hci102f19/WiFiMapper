import json

for n in json.load(open('./wifis/GroundFloor.json', 'r')):
    print(f'new Node("{n["mac"]}", {n["lat"]}, {n["lon"]}),')
