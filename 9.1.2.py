import csv

with open('wares.csv', encoding='utf8') as f:
    reader = csv.reader(f, delimiter=';', quotechar='"')
    sort_data = sorted([row for row in reader], key=lambda x: int(x[1]))
    summ = 1000
    card = []
    for item in sort_data:
        for i in range(10):
            if summ >= int(item[1]):
                summ -= int(item[1])
                card.append(item[0])
    if card:
        print(', '.join(card))
    else:
        print('error')
