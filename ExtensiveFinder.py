import re
import sys
import requests
from requests.adapters import HTTPAdapter, Retry
import urllib.parse
import csv

re_next_link = re.compile(r'<(.+)>; rel="next"')
retries = Retry(total=5, backoff_factor=0.25, status_forcelist=[500, 502, 503, 504])
session = requests.Session()
session.mount("https://", HTTPAdapter(max_retries=retries))

def get_next_link(headers):
    if "Link" in headers:
        match = re_next_link.match(headers["Link"])
        if match:
            return match.group(1)

def get_batch(batch_url):
    while batch_url:
        response = session.get(batch_url)
        response.raise_for_status()
        total = response.headers["x-total-results"]
        yield response, total
        batch_url = get_next_link(response.headers)

if len(sys.argv) != 3:
    print("Usage: python script.py <protein_name> <organism_name>")
    sys.exit(1)

protein_name = sys.argv[1]
organism_name = sys.argv[2]

url = 'https://rest.uniprot.org/uniprotkb/search?format=tsv&includeIsoform=false&query='
url2 = urllib.parse.quote(protein_name) + '%28taxonomy_id%3A9606%29&size=500'

url += url2

progress = 0

with open('protein.tsv', 'a') as f:
    for batch, total in get_batch(url):
        lines = batch.text.splitlines()
        if not progress:
            print(lines[0], file=f)
        for line in lines[1:]:
            print(line, file=f)
        progress += len(lines[1:])
        print(f'{progress} / {total}')






