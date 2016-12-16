import csv

def overlap_to_html(category):
    with open('data/{}-overlap.csv'.format(category), 'r') as input:
        reader = csv.DictReader(input)
        rows = list(reader)

    output = '<link rel="stylesheet" href="style.css"><table>'

    for row in rows:
        output += '<tr><td>{}</td>'.format(row['year'])
        for i in range(int(row['# finalist for pulitzer only'])):
            output += '<td class="pulitzer">&nbsp;</td>'
        winner = (row['shared winner'] == '1')
        for i in range(int(row['# finalist for both'])):
            if winner:
                output +='<td class="both">w</td>'
                winner = False
            else:
                output += '<td class="both">&nbsp;</td>'
        for i in range(int(row['# finalist for nba only'])):
            output += '<td class="nba">&nbsp;</td>'
        output += '</tr>'

    output += '</table>'

    filename = '{}-overlap.html'.format(category)
    with open(filename, 'w') as outfile:
        outfile.write(output)
    print('wrote to', filename)

overlap_to_html('fiction')
overlap_to_html('poetry')
