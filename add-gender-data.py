import csv

from gender import analyze_name

def transform(prize):
    with open ('data/{}.csv'.format(prize), 'r') as inputfile:
        reader = csv.DictReader(inputfile)
        rows = list(reader)

    for row in rows:
        first_name = row['author'].split()[0]
        row['gender'], gender_prob = analyze_name(first_name)
        if int(gender_prob) < 90:
            print(row, gender_prob)

    filename = 'data/{}-gendered.csv'.format(prize)
    with open(filename, 'w', newline='') as outputfile:
        writer = csv.DictWriter(outputfile, fieldnames=['year', 'category', 'prize', 'outcome', 'author', 'title', 'gender'])
        writer.writeheader()
        writer.writerows(rows)
    print('wrote to', filename)

transform('pulitzer')
transform('nba')
