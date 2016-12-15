import csv
from os import path

with open ('data/raw/nb-1984-2010-from-pdf.txt', 'r') as input:
    lines = input.readlines()

lines = [line.strip() for line in lines]
result = []

def process(year, category, outcome, line):
    if year <= 2004:
        author, title = line.split(' – ')
    elif year <= 2006 and outcome == 'winner':
        author, title = line.split(' - ')
    else:
        fields = line.split(', ')
        author = fields[0]
        title = ', '.join(fields[1:])
    result.append([year, category, 'nba', outcome, author, title])

i = 0
while i < len(lines):
    line = lines[i]
    if line == 'FICTION' or line == 'POETRY':
        category = line.lower()
        year = int(lines[i - 1])
        i += 1
        line = lines[i]
        process(year, category, 'winner', line)
        while True:
            i += 1
            line = lines[i]
            if line[0].isdigit(): break
            process(year, category, 'finalist', line)
    i += 1

filename = path.join('data', 'nba.csv')
with open(filename, 'w', newline='') as output:
    writer = csv.writer(output)
    writer.writerow(['year', 'category', 'prize', 'outcome', 'author', 'title'])
    writer.writerows(result)
