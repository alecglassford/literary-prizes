import csv
from os import path

with open(path.join('data', 'pulitzer.csv'), 'r') as input:
    reader = csv.DictReader(input)
    pulitzers = list(reader)

with open(path.join('data', 'nba.csv'), 'r') as input:
    reader = csv.DictReader(input)
    nbas = list(reader)

p_years = set([e['year'] for e in pulitzers])
n_years = set([e['year'] for e in nbas])
years = p_years.intersection(n_years)

def overlap(year, category):

    p_sample = [e for e in pulitzers if e['year'] == year and e['category'] == category]
    n_sample = [e for e in nbas if e['year'] == year and e['category'] == category]
    num_p, num_both, num_n = 0, 0 , 0

    p_titles = set([e['title'] for e in p_sample])
    n_titles = set([e['title'] for e in n_sample])
    both_titles = p_titles.intersection(n_titles)
    p_authors = set([e['author'] for e in p_sample])
    n_authors = set([e['author'] for e in n_sample])
    both_authors = p_authors.intersection(n_authors)
    if len(both_titles) != len(both_authors):
        print('DEBUG ME!', both_titles, both_authors)
    return(year, len(p_titles) - len(both_titles), len(both_titles), len(n_titles) - len(both_titles))

def overlap_category(category):
    p_years = set([e['year'] for e in pulitzers if e['category'] == category])
    n_years = set([e['year'] for e in nbas if e['category'] == category])
    years = p_years.intersection(n_years)
    years = sorted(list(years))
    result = []
    for year in years:
        result.append(overlap(year, category))
    filename = path.join('data', '{}-overlap.csv'.format(category))
    with open(filename, 'w', newline='') as output:
        writer = csv.writer(output)
        writer.writerow(['year', '# finalist for pulitzer only', '# finalist for both', '# finalist for nba only'])
        writer.writerows(result)
    print('done writing to', filename)

overlap_category('fiction')
overlap_category('poetry')
