from scanner import Scanner

scanner = Scanner()
spots = [x for x in scanner.scan()]
sorted_spots = sorted(spots, key=lambda x: x['signal'], reverse=True)

print(sorted_spots)
