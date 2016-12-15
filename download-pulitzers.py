import csv
from html import unescape
import json
from os import makedirs, path
from time import sleep

import requests

categories = {'fiction': 219, 'poetry': 224}

base_urls = {'winner': 'http://www.pulitzer.org/cache/api/1/winners/cat/{}/raw.json',
             'finalist': 'http://www.pulitzer.org/cache/api/1/finalist/{}/all/raw.json'}

raw_path = path.join('data', 'raw')
makedirs(raw_path, exist_ok=True)

result = []

def fetch (category, outcome):
    filename = path.join(raw_path, '{}-{}.json'.format(category, outcome))
    if path.exists(filename):
        print('already have a copy of', category, outcome, 'raw file')
        return
    url = base_urls[outcome].format(categories[category])
    resp = requests.get(url)
    data = resp.json()
    while not data:
        print (url, 'gave an empty JSON :(')
        sleep(1)
        resp = requests.get(url)
        data = resp.json()
    print('got data from', url)
    with open(filename, 'w') as raw_file:
        json.dump(data, raw_file)

def process (category, outcome):
    filename = path.join(raw_path, '{}-{}.json'.format(category, outcome))
    with open(filename, 'r') as raw_file:
        data = json.load(raw_file)
    for entry in data:
        author = entry['title']
        try:
            title = unescape(entry['field_publication']['und'][0]['safe_value']).strip()
        except:
            title = 'No award'
        year = 2120 - int(entry['field_year']['und'][0]['tid'])
        result.append([year, category, 'pulitzer', outcome, author, title])
    print('processed', category, outcome)

for category in categories:
    for outcome in base_urls:
        fetch(category, outcome)
        process(category, outcome)

def recent (entry):
    return (entry[1] == 'fiction' and entry[0] >= 1984) or \
           (entry[1] == 'poetry' and entry[0] >= 1991)

result = filter(recent, result)
filename = path.join('data', 'pulitzer.csv')
with open(filename, 'w', newline='') as output:
    writer = csv.writer(output)
    writer.writerow(['year', 'category', 'prize', 'outcome', 'author', 'title'])
    writer.writerows(result)
