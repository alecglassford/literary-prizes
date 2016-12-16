from collections import Counter
import csv
from os import path

GENDER_DIR = 'data'

filename = path.join(GENDER_DIR, 'wrangledbabynames.csv')
index = {}

def build_index():
    with open(filename, 'r') as load_file:
        reader = csv.DictReader(load_file)
        for row in reader:
            lower_name = row['name'].lower()
            index[lower_name] = row['gender'], row['ratio']

def analyze_name(name):
    if not index:
        build_index()
    lower_name = name.lower()
    if lower_name in index:
        return index[lower_name]
    return 'U', -1 # U means gender is unclassified, -1 means undefined
