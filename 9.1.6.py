import csv

import sys

with open('plantis.csv', 'w', newline='', encoding="utf8") as csvfile:
    writer = csv.writer(
        csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL
    )
    writer.writerow(
        'nomen, definitio, pluma, Russian nomen, '
        'familia, Russian nomen familia'.split(', ')
    )
    data = [line.strip().split('\t') for line in sys.stdin]
    for row in data:
        writer.writerow(row)
