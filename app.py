import json

from scanner import Scanner

scanner = Scanner()

i = 0
running = True
while running:
    test = input("Start scan (y/n): ")
    if test.lower() == 'y':
        print("Scanning...")
        json.dump(scanner.scan(), open('./output/{}.json'.format(i), 'w'))
        print("Done: {}".format(i))
        i += 1
    elif test.lower() == 'n':
        running = False
