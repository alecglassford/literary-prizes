import csv

def overlap_to_html(category):
    with open('data/{}-overlap.csv'.format(category), 'r') as input:
        reader = csv.DictReader(input)
        rows = list(reader)

    left_len = max([int(row['# finalist for pulitzer only']) for row in rows])
    middle_len = max([int(row['# finalist for both']) for row in rows])
    right_len = max([int(row['# finalist for nba only']) for row in rows])

    output = '<link rel="stylesheet" href="style.css"><table>'

    for row in rows:
        output += '<tr><td>{}</td>'.format(row['year'])

        count = int(row['# finalist for pulitzer only'])
        space = left_len - count
        for i in range(count):
            output += '<td class="pulitzer">&nbsp;</td>'
        for i in range(space):
            output += '<td>&nbsp;</td>'

        output += '<td>&nbsp;</td>'

        count = int(row['# finalist for both'])
        space = middle_len - count
        first_space = space // 2
        second_space = space - first_space
        for i in range(first_space):
            output += '<td>&nbsp;</td>'

        winner = (row['shared winner'] == '1')
        for i in range(count):
            if winner:
                output +='<td class="both">w</td>'
                winner = False
            else:
                output += '<td class="both">&nbsp;</td>'
        for i in range(second_space):
            output += '<td>&nbsp;</td>'

        output += '<td>&nbsp;</td>'
        count = int(row['# finalist for nba only'])
        space = right_len - count
        for i in range(space):
            output += '<td>&nbsp;</td>'
        for i in range(count):
            output += '<td class="nba">&nbsp;</td>'
        output += '</tr>'

    output += '</table>'

    filename = '{}-overlap-split.html'.format(category)
    with open(filename, 'w') as outfile:
        outfile.write(output)
    print('wrote to', filename)

overlap_to_html('fiction')
overlap_to_html('poetry')
