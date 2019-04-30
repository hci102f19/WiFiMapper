import subprocess
from time import sleep

import re


class Scanner(object):
    def __init__(self):
        self.cmd = "sudo iwlist wlan0 scanning | egrep 'Cell |Frequency|Quality|ESSID'"

        self.essid_regex = re.compile(r'ESSID:"(.*)"')
        self.signal_regex = re.compile(r'Signal level=(-\d+)')
        self.quality_regex = re.compile(r'Quality=(\d+)\/(\d+)')
        self.mac_regex = re.compile(r'Address: (([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2}))')
        self.frequency_regex = re.compile(r'Frequency:([0-9.]+) GHz')

    def scan(self):
        scans = []
        for x in range(10):
            output = subprocess.getoutput(self.cmd)
            scans.append(self.parse_output(output))
            sleep(0.25)
        return scans

    def parse_output(self, output):
        networks = []
        cur_package = ""
        for line in output.split('\n'):
            line = line.strip()
            if line[0:4] == 'Cell':
                if cur_package:
                    networks.append(self.parse_network(cur_package))
                    cur_package = ""
            cur_package += "{}\n".format(line)

        if cur_package:
            networks.append(self.parse_network(cur_package))

        return networks

    def parse_network(self, cur_package):
        essid = self.essid_regex.search(cur_package)
        signal = self.signal_regex.search(cur_package)
        quality = self.quality_regex.search(cur_package)
        mac = self.mac_regex.search(cur_package)
        frequency = self.frequency_regex.search(cur_package)

        return {
            'essid': essid.group(1),
            'mac': mac.group(1),
            'signal': int(signal.group(1)),
            'quality': round((int(quality.group(1)) / int(quality.group(2))) * 100, 2),
            'frequency': int(round(float(frequency.group(1)) * 1000, 0))
        }
