import csv

number = int(input())

with open('vps.csv', encoding='utf8') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=';', quotechar='"')
    filtered_data = list(
        map(
            lambda q: q['Специальность'],
            filter(lambda x: int(x['соответствует в %']) >= number, reader),
        )
    )
    print(*filtered_data, sep='\n')
