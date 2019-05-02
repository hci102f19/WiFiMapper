import json
import os
from time import sleep

from scanner import Scanner

scanner = Scanner()

while True:
    spots = [x for x in scanner.scan() if x['essid'] == "AAU-1x"]
    sorted_spots = sorted(spots, key=lambda x: x['signal'], reverse=True)

    os.system('cls' if os.name == 'nt' else 'clear')
    print(json.dumps(sorted_spots[0], indent=4))
